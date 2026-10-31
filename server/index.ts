import express, { Request, Response } from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import path from 'node:path';
import fs from 'node:fs';
import { execFileSync } from 'node:child_process';
import { DatabaseSync } from 'node:sqlite';
import {
  CreateQuestionSchema,
  GenerateBriefSchema,
  ManualObservationSchema,
  TriggerVisibilityRunSchema,
  UpdateCitationSchema,
  UpdateContentPageSchema,
  UpdateLaunchTaskSchema,
} from './schemas.ts';

dotenv.config();

const ROOT_DIR = process.cwd();
const DEFAULT_DB_PATH = path.resolve(ROOT_DIR, process.env.SQLITE_DB_PATH || './data/incubrix.db');

export function getDb(customPath?: string): DatabaseSync {
  const dbPath = customPath || DEFAULT_DB_PATH;
  fs.mkdirSync(path.dirname(dbPath), { recursive: true });
  const db = new DatabaseSync(dbPath);
  db.exec('PRAGMA journal_mode=WAL;');
  db.exec('PRAGMA foreign_keys=ON;');
  return db;
}

function runPythonInline(script: string, args: string[] = []): any {
  const output = execFileSync('python', ['-X', 'utf8', '-c', script, ...args], {
    cwd: ROOT_DIR,
    encoding: 'utf-8',
    timeout: 45000,
  });
  return JSON.parse(output.trim());
}

export function createApp(customDbPath?: string) {
  const app = express();
  app.use(cors());
  app.use(express.json({ limit: '5mb' }));

  const dbArgs = customDbPath ? [customDbPath] : [];

  // Health Check
  app.get('/api/health', (_req: Request, res: Response) => {
    res.json({ status: 'ok', target: 'https://www.incubrix.com', timestamp: new Date().toISOString() });
  });

  // 1. Overview Dashboard Metrics (calculated strictly from SQLite records, excluding DEMO)
  app.get('/api/overview', (_req: Request, res: Response) => {
    try {
      const data = runPythonInline(
        `import sys, json; from engine.reporting import compute_overview_metrics; db = sys.argv[1] if len(sys.argv) > 1 else None; print(json.dumps(compute_overview_metrics(db)))`,
        dbArgs
      );
      res.json(data);
    } catch (err: any) {
      res.status(500).json({ error: err.message || 'Failed to compute overview metrics' });
    }
  });

  // 2. Research Questions (100+ Creator Questions + Deduplication & Provenance)
  app.get('/api/questions', (req: Request, res: Response) => {
    const db = getDb(customDbPath);
    try {
      const { category, search, intent, market, evidence_tier } = req.query;
      let sql = 'SELECT * FROM questions WHERE 1=1';
      const params: any[] = [];

      if (evidence_tier && evidence_tier !== 'all') {
        sql += ' AND evidence_tier = ?';
        params.push(String(evidence_tier));
      } else {
        sql += ' AND is_demo = 0';
      }

      if (category && category !== 'all') {
        sql += ' AND category = ?';
        params.push(String(category));
      }
      if (intent && intent !== 'all') {
        sql += ' AND search_intent = ?';
        params.push(String(intent));
      }
      if (market && market !== 'all') {
        sql += ' AND target_markets_json LIKE ?';
        params.push(`%"${String(market)}"%`);
      }
      if (search && String(search).trim()) {
        sql += ' AND (canonical_question LIKE ? OR original_wording LIKE ? OR id LIKE ?)';
        const term = `%${String(search).trim()}%`;
        params.push(term, term, term);
      }
      sql += ' ORDER BY id ASC';

      const rows = db.prepare(sql).all(...params) as any[];
      const parsed = rows.map((r) => ({
        ...r,
        evidence_tier: r.evidence_tier || 'AWAITING_MEASUREMENT',
        reference_metadata: JSON.parse(r.reference_metadata_json || '{}'),
        target_markets: JSON.parse(r.target_markets_json || '["US"]'),
        provenance_sources: JSON.parse(r.provenance_sources_json || '[]'),
      }));

      const countRows = db.prepare('SELECT evidence_tier, COUNT(*) as cnt FROM questions GROUP BY evidence_tier').all() as any[];
      const tierCounts: Record<string, number> = {
        total_prepared: 100,
        genuine_verified: 0,
        partially_measured: 0,
        reference_only: 0,
        awaiting_measurement: 0,
        demo: 0,
      };
      for (const cr of countRows) {
        const k = String(cr.evidence_tier || '').toLowerCase();
        if (k in tierCounts) {
          tierCounts[k] = Number(cr.cnt);
        }
      }

      res.json({ count: parsed.length, tier_counts: tierCounts, questions: parsed });
    } finally {
      db.close();
    }
  });

  // Add or deduplicate a question preserving provenance
  app.post('/api/questions', (req: Request, res: Response) => {
    const parsed = CreateQuestionSchema.safeParse(req.body);
    if (!parsed.success) {
      res.status(400).json({ error: 'Validation failed', details: parsed.error.flatten() });
      return;
    }

    try {
      const payloadStr = JSON.stringify(parsed.data);
      const result = runPythonInline(
        `
import sys, json
from engine.db import get_connection, now_iso
from engine.questions_seed import normalize_question_fingerprint, validate_question_record

payload = json.loads(sys.argv[1])
db_path = sys.argv[2] if len(sys.argv) > 2 else None
is_valid, errs = validate_question_record(payload)
if not is_valid:
    raise ValueError("; ".join(errs))

fp = normalize_question_fingerprint(payload["canonical_question"])
conn = get_connection(db_path)
ts = now_iso()
existing = conn.execute("SELECT * FROM questions WHERE normalized_fingerprint = ?", (fp,)).fetchone()
prov_entry = {
    "source_url": payload["source_url"],
    "source_type": payload["source_type"],
    "collection_date": payload["collection_date"],
    "original_wording": payload["original_wording"],
}
if existing:
    prov = json.loads(existing["provenance_sources_json"] or "[]")
    if not any(p.get("source_url") == prov_entry["source_url"] and p.get("original_wording") == prov_entry["original_wording"] for p in prov):
        prov.append(prov_entry)
    merge_cnt = max(0, len(prov) - 1)
    conn.execute("UPDATE questions SET provenance_sources_json = ?, duplicate_merge_count = ?, updated_at = ? WHERE id = ?", (json.dumps(prov), merge_cnt, ts, existing["id"]))
    conn.commit()
    row = dict(conn.execute("SELECT * FROM questions WHERE id = ?", (existing["id"],)).fetchone())
    conn.close()
    print(json.dumps({"action": "merged_into_existing_preserving_provenance", "question": row}))
else:
    cnt = conn.execute("SELECT COUNT(*) AS c FROM questions").fetchone()["c"]
    new_id = f"Q-{cnt + 1:03d}"
    conn.execute("""
        INSERT INTO questions (
            id, canonical_question, normalized_fingerprint, original_wording,
            category, search_intent, target_persona, source_url, source_type,
            collection_date, validation_status, validation_notes, priority_score,
            target_markets_json, provenance_sources_json, duplicate_merge_count,
            is_demo, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'validated', 'Validated via API', ?, ?, ?, 0, 0, ?, ?)
    """, (
        new_id, payload["canonical_question"], fp, payload["original_wording"],
        payload["category"], payload["search_intent"], payload["target_persona"],
        payload["source_url"], payload["source_type"], payload["collection_date"],
        payload["priority_score"], json.dumps(payload["target_markets"]),
        json.dumps([prov_entry]), ts, ts
    ))
    conn.commit()
    row = dict(conn.execute("SELECT * FROM questions WHERE id = ?", (new_id,)).fetchone())
    conn.close()
    print(json.dumps({"action": "created_new", "question": row}))
        `,
        [payloadStr, ...dbArgs]
      );
      res.status(201).json(result);
    } catch (err: any) {
      res.status(400).json({ error: err.message || 'Failed to add question' });
    }
  });

  // 3. Visibility Observations & Multi-Date Comparison
  app.get('/api/visibility/observations', (req: Request, res: Response) => {
    const db = getDb(customDbPath);
    try {
      const { provider, market, status, date, include_demo, question_id } = req.query;
      let sql = 'SELECT * FROM visibility_observations WHERE 1=1';
      const params: any[] = [];

      if (include_demo !== 'true') {
        sql += ' AND is_demo = 0';
      }
      if (provider && provider !== 'all') {
        sql += ' AND provider = ?';
        params.push(String(provider));
      }
      if (market && market !== 'all') {
        sql += ' AND market = ?';
        params.push(String(market));
      }
      if (status && status !== 'all') {
        sql += ' AND collection_status = ?';
        params.push(String(status));
      }
      if (date && date !== 'all') {
        sql += ' AND observation_date = ?';
        params.push(String(date));
      }
      if (question_id) {
        sql += ' AND question_id = ?';
        params.push(String(question_id));
      }
      sql += ' ORDER BY observation_date DESC, question_id ASC, provider ASC, pass_number ASC';

      const rows = db.prepare(sql).all(...params) as any[];
      const parsed = rows.map((r) => ({
        ...r,
        incubrix_citation_urls: JSON.parse(r.incubrix_citation_urls_json || '[]'),
        competitors_mentioned: JSON.parse(r.competitors_mentioned_json || '[]'),
        citations_found: JSON.parse(r.citations_found_json || '[]'),
      }));
      res.json({ count: parsed.length, observations: parsed });
    } finally {
      db.close();
    }
  });

  app.get('/api/visibility/compare', (req: Request, res: Response) => {
    try {
      const dateA = String(req.query.date_a || '2026-10-24');
      const dateB = String(req.query.date_b || '2026-10-25');
      const data = runPythonInline(
        `import sys, json; from engine.visibility import compare_observations_across_dates; db = sys.argv[3] if len(sys.argv) > 3 else None; print(json.dumps(compare_observations_across_dates(sys.argv[1], sys.argv[2], db)))`,
        [dateA, dateB, ...dbArgs]
      );
      res.json(data);
    } catch (err: any) {
      res.status(500).json({ error: err.message });
    }
  });

  // Record Manual Evidence Observation
  app.post('/api/visibility/manual', (req: Request, res: Response) => {
    const parsed = ManualObservationSchema.safeParse(req.body);
    if (!parsed.success) {
      res.status(400).json({ error: 'Validation failed', details: parsed.error.flatten() });
      return;
    }
    try {
      const result = runPythonInline(
        `import sys, json; from engine.visibility import record_manual_observation; db = sys.argv[2] if len(sys.argv) > 2 else None; print(json.dumps(record_manual_observation(json.loads(sys.argv[1]), db)))`,
        [JSON.stringify(parsed.data), ...dbArgs]
      );
      res.status(201).json(result);
    } catch (err: any) {
      res.status(400).json({ error: err.message });
    }
  });

  // Reload Built-in Manual Research Evidence
  app.post('/api/visibility/reload-manual', (_req: Request, res: Response) => {
    try {
      const result = runPythonInline(
        `import sys, json; from engine.seed_manual_research_evidence import load_manual_research_evidence; db = sys.argv[1] if len(sys.argv) > 1 else None; print(json.dumps(load_manual_research_evidence(db or "data/incubrix.db")))`,
        [...dbArgs]
      );
      res.json(result);
    } catch (err: any) {
      res.status(500).json({ error: err.message });
    }
  });

  // Trigger Visibility Engine Run
  app.post('/api/visibility/run', (req: Request, res: Response) => {
    const parsed = TriggerVisibilityRunSchema.safeParse(req.body || {});
    if (!parsed.success) {
      res.status(400).json({ error: 'Validation failed', details: parsed.error.flatten() });
      return;
    }
    try {
      const result = runPythonInline(
        `
import sys, json
from engine.visibility import execute_visibility_run
cfg = json.loads(sys.argv[1])
db = sys.argv[2] if len(sys.argv) > 2 else None
res = execute_visibility_run(
    mode=cfg["mode"],
    markets=cfg["markets"],
    providers=cfg["providers"],
    limit=cfg["limit"],
    pass_number=cfg["pass_number"],
    custom_db_path=db
)
print(json.dumps(res))
        `,
        [JSON.stringify(parsed.data), ...dbArgs]
      );
      res.json(result);
    } catch (err: any) {
      res.status(500).json({ error: err.message });
    }
  });

  // 4. Technical SEO Audit & Crawled Pages
  app.get('/api/audit', (_req: Request, res: Response) => {
    const db = getDb(customDbPath);
    try {
      const issues = db.prepare('SELECT * FROM technical_issues ORDER BY priority_rank ASC').all() as any[];
      const pagesRaw = db.prepare('SELECT * FROM crawled_pages ORDER BY url ASC').all() as any[];
      const pages = pagesRaw.map((p) => ({
        ...p,
        h1_tags: JSON.parse(p.h1_tags_json || '[]'),
        h2_tags: JSON.parse(p.h2_tags_json || '[]'),
        json_ld_blocks: JSON.parse(p.json_ld_blocks_json || '[]'),
        og_tags: JSON.parse(p.og_tags_json || '{}'),
        twitter_tags: JSON.parse(p.twitter_tags_json || '{}'),
        internal_links: JSON.parse(p.internal_links_json || '[]'),
      }));
      res.json({ issues_count: issues.length, pages_count: pages.length, issues, crawled_pages: pages });
    } finally {
      db.close();
    }
  });

  app.post('/api/audit/run', (req: Request, res: Response) => {
    try {
      const fetchLive = req.body?.fetch_live !== false;
      const result = runPythonInline(
        `import sys, json; from engine.auditor import run_live_website_audit; db = sys.argv[2] if len(sys.argv) > 2 else None; print(json.dumps(run_live_website_audit(fetch_live=(sys.argv[1]=='true'), validate_patches=True, custom_db_path=db)))`,
        [String(fetchLive), ...dbArgs]
      );
      res.json(result);
    } catch (err: any) {
      res.status(500).json({ error: err.message });
    }
  });

  // Validate a specific JSON-LD snippet or issue patch
  app.post('/api/audit/validate-jsonld', (req: Request, res: Response) => {
    const rawJson = String(req.body?.json_ld || '');
    try {
      const result = runPythonInline(
        `import sys, json; from engine.auditor import validate_json_ld; ok, errs = validate_json_ld(sys.argv[1]); print(json.dumps({"valid": ok, "errors": errs}))`,
        [rawJson]
      );
      res.json(result);
    } catch (err: any) {
      res.status(400).json({ error: err.message });
    }
  });

  // 5. Content Studio (10 Pages + Editor + Brief Generator + Export)
  app.get('/api/content', (_req: Request, res: Response) => {
    const db = getDb(customDbPath);
    try {
      const rows = db.prepare('SELECT * FROM content_pages ORDER BY page_id ASC').all() as any[];
      const pages = rows.map((p) => ({
        ...p,
        target_question_ids: JSON.parse(p.target_question_ids_json || '[]'),
        supporting_questions: JSON.parse(p.supporting_questions_json || '[]'),
        headings: JSON.parse(p.headings_json || '[]'),
        citations: JSON.parse(p.citations_json || '[]'),
        internal_links: JSON.parse(p.internal_links_json || '[]'),
        verification_checklist: JSON.parse(p.verification_checklist_json || '[]'),
        unverified_claims_flagged: JSON.parse(p.unverified_claims_flagged_json || '[]'),
      }));
      res.json({ count: pages.length, pages });
    } finally {
      db.close();
    }
  });

  app.put('/api/content/:pageId', (req: Request, res: Response) => {
    const parsed = UpdateContentPageSchema.safeParse(req.body);
    if (!parsed.success) {
      res.status(400).json({ error: 'Content validation failed', details: parsed.error.flatten() });
      return;
    }
    const pageId = String(req.params.pageId);
    try {
      const result = runPythonInline(
        `
import sys, json
from engine.db import get_connection, now_iso
from engine.auditor import validate_json_ld
from engine.content_studio import export_content_page_files

page_id = sys.argv[1]
payload = json.loads(sys.argv[2])
db_path = sys.argv[3] if len(sys.argv) > 3 else None

ok, errs = validate_json_ld(payload["json_ld_schema"])
if not ok:
    raise ValueError("Invalid JSON-LD: " + "; ".join(errs))

conn = get_connection(db_path)
wc = len(payload["body_markdown"].split())
conn.execute("""
    UPDATE content_pages
    SET title = ?, meta_description = ?, direct_answer_summary = ?,
        body_markdown = ?, json_ld_schema = ?, status = ?,
        word_count = ?, updated_at = ?
    WHERE page_id = ?
""", (
    payload["title"], payload["meta_description"], payload["direct_answer_summary"],
    payload["body_markdown"], payload["json_ld_schema"], payload["status"],
    wc, now_iso(), page_id
))
conn.commit()
row = dict(conn.execute("SELECT * FROM content_pages WHERE page_id = ?", (page_id,)).fetchone())
conn.close()
export_content_page_files(page_id, db_path)
print(json.dumps(row))
        `,
        [pageId, JSON.stringify(parsed.data), ...dbArgs]
      );
      res.json(result);
    } catch (err: any) {
      res.status(400).json({ error: err.message });
    }
  });

  app.post('/api/content/generate-brief', (req: Request, res: Response) => {
    const parsed = GenerateBriefSchema.safeParse(req.body);
    if (!parsed.success) {
      res.status(400).json({ error: 'Invalid brief request', details: parsed.error.flatten() });
      return;
    }
    try {
      const result = runPythonInline(
        `import sys, json; from engine.content_studio import generate_content_brief; db = sys.argv[3] if len(sys.argv) > 3 else None; print(json.dumps(generate_content_brief(sys.argv[1], sys.argv[2], db)))`,
        [parsed.data.question_id, parsed.data.content_type, ...dbArgs]
      );
      res.json(result);
    } catch (err: any) {
      res.status(400).json({ error: err.message });
    }
  });

  app.get('/api/content/:pageId/export', (req: Request, res: Response) => {
    try {
      const pageId = String(req.params.pageId);
      const result = runPythonInline(
        `import sys, json; from engine.content_studio import export_content_page_files; db = sys.argv[2] if len(sys.argv) > 2 else None; print(json.dumps(export_content_page_files(sys.argv[1], db)))`,
        [pageId, ...dbArgs]
      );
      res.json(result);
    } catch (err: any) {
      res.status(404).json({ error: err.message });
    }
  });

  // 6. Citation Opportunities (30 Specific Third-Party Pages)
  app.get('/api/citations', (req: Request, res: Response) => {
    const db = getDb(customDbPath);
    try {
      const { source_type, tier } = req.query;
      let sql = 'SELECT * FROM citation_opportunities WHERE 1=1';
      const params: any[] = [];
      if (source_type && source_type !== 'all') {
        sql += ' AND source_type = ?';
        params.push(String(source_type));
      }
      if (tier && tier !== 'all') {
        sql += ' AND priority_tier = ?';
        params.push(String(tier));
      }
      sql += ' ORDER BY opportunity_id ASC';
      const rows = db.prepare(sql).all(...params) as any[];
      const citations = rows.map((c) => ({
        ...c,
        competitor_mentions: JSON.parse(c.competitor_mentions_json || '[]'),
      }));
      res.json({ count: citations.length, citations });
    } finally {
      db.close();
    }
  });

  app.patch('/api/citations/:id', (req: Request, res: Response) => {
    const parsed = UpdateCitationSchema.safeParse(req.body);
    if (!parsed.success) {
      res.status(400).json({ error: 'Invalid citation update', details: parsed.error.flatten() });
      return;
    }
    const db = getDb(customDbPath);
    try {
      const id = String(req.params.id);
      const existing = db.prepare('SELECT * FROM citation_opportunities WHERE opportunity_id = ?').get(id) as any;
      if (!existing) {
        res.status(404).json({ error: 'Citation opportunity not found' });
        return;
      }
      db.prepare(
        'UPDATE citation_opportunities SET verification_status = ?, priority_tier = ?, notes = ? WHERE opportunity_id = ?'
      ).run(
        parsed.data.verification_status,
        parsed.data.priority_tier || existing.priority_tier,
        parsed.data.notes ?? existing.notes,
        id
      );
      const updated = db.prepare('SELECT * FROM citation_opportunities WHERE opportunity_id = ?').get(id);
      res.json(updated);
    } finally {
      db.close();
    }
  });

  // 7. Weekly Reports & 90-Day Launch Plan
  app.get('/api/reports', (_req: Request, res: Response) => {
    const db = getDb(customDbPath);
    try {
      const reportsRaw = db.prepare('SELECT * FROM weekly_reports ORDER BY generated_at DESC').all() as any[];
      const reports = reportsRaw.map((r) => ({
        ...r,
        metrics_snapshot: JSON.parse(r.metrics_snapshot_json || '{}'),
      }));
      res.json({ count: reports.length, reports });
    } finally {
      db.close();
    }
  });

  app.post('/api/reports/generate', (_req: Request, res: Response) => {
    try {
      const result = runPythonInline(
        `import sys, json; from engine.reporting import generate_weekly_report; db = sys.argv[1] if len(sys.argv) > 1 else None; print(json.dumps(generate_weekly_report(db)))`,
        dbArgs
      );
      res.json(result);
    } catch (err: any) {
      res.status(500).json({ error: err.message });
    }
  });

  app.get('/api/launch-plan', (_req: Request, res: Response) => {
    const db = getDb(customDbPath);
    try {
      const tasks = db.prepare('SELECT * FROM launch_plan_tasks ORDER BY week_number ASC').all() as any[];
      res.json({ count: tasks.length, tasks });
    } finally {
      db.close();
    }
  });

  app.patch('/api/launch-plan/:taskId', (req: Request, res: Response) => {
    const parsed = UpdateLaunchTaskSchema.safeParse(req.body);
    if (!parsed.success) {
      res.status(400).json({ error: 'Validation failed', details: parsed.error.flatten() });
      return;
    }
    const db = getDb(customDbPath);
    try {
      const taskId = String(req.params.taskId);
      const existing = db.prepare('SELECT * FROM launch_plan_tasks WHERE task_id = ?').get(taskId) as any;
      if (!existing) {
        res.status(404).json({ error: 'Task not found' });
        return;
      }
      db.prepare('UPDATE launch_plan_tasks SET status = ?, measured_metric = ? WHERE task_id = ?').run(
        parsed.data.status,
        parsed.data.measured_metric || existing.measured_metric,
        taskId
      );
      const updated = db.prepare('SELECT * FROM launch_plan_tasks WHERE task_id = ?').get(taskId);
      res.json(updated);
    } finally {
      db.close();
    }
  });

  // 8. Settings, Data Sources, Engine Runs & CSV/Workbook Exports
  app.get('/api/settings', (_req: Request, res: Response) => {
    const db = getDb(customDbPath);
    try {
      const providers = runPythonInline(
        `import json; from engine.visibility import check_provider_Statuses; print(json.dumps(check_provider_Statuses()))`
      );
      const runsRaw = db.prepare('SELECT * FROM engine_runs ORDER BY started_at DESC LIMIT 20').all() as any[];
      const runs = runsRaw.map((r) => ({
        ...r,
        markets: JSON.parse(r.markets_json || '[]'),
        providers: JSON.parse(r.providers_json || '[]'),
        logs: JSON.parse(r.log_summary_json || '[]'),
      }));
      res.json({
        target_website: 'https://www.incubrix.com',
        canonical_domain: 'https://incubrix.com/',
        supported_markets: [
          { code: 'US', label: 'United States (en-US, gl=us, hl=en)' },
          { code: 'IN', label: 'India (en-IN, gl=in, hl=en)' },
          { code: 'GB', label: 'United Kingdom (en-GB, gl=uk, hl=en)' },
        ],
        providers,
        runs,
        scheduler_command: 'python -m engine.cli run-visibility --mode live --markets US,IN,GB --limit 100 --pass-number 1',
      });
    } finally {
      db.close();
    }
  });

  app.get('/api/exports/visibility.csv', (req: Request, res: Response) => {
    try {
      const includeDemo = req.query.include_demo === 'true';
      runPythonInline(
        `import sys; from pathlib import Path; from engine.visibility import export_visibility_to_csv; db = sys.argv[2] if len(sys.argv) > 2 else None; export_visibility_to_csv(Path('exports/visibility_observations.csv'), include_demo=(sys.argv[1]=='true'), custom_db_path=db); print('{"ok":true}')`,
        [String(includeDemo), ...dbArgs]
      );
      const csvPath = path.resolve(ROOT_DIR, 'exports/visibility_observations.csv');
      res.setHeader('Content-Type', 'text/csv; charset=utf-8');
      res.setHeader('Content-Disposition', 'attachment; filename="incubrix_visibility_observations.csv"');
      res.sendFile(csvPath);
    } catch (err: any) {
      res.status(500).json({ error: err.message });
    }
  });

  app.get('/api/exports/questions.csv', (_req: Request, res: Response) => {
    const csvPath = path.resolve(ROOT_DIR, 'exports/creator_questions_100.csv');
    res.setHeader('Content-Type', 'text/csv; charset=utf-8');
    res.setHeader('Content-Disposition', 'attachment; filename="incubrix_creator_questions_100.csv"');
    res.sendFile(csvPath);
  });

  app.get('/api/exports/citations.csv', (_req: Request, res: Response) => {
    const csvPath = path.resolve(ROOT_DIR, 'exports/citations/CITATION_TARGETS.csv');
    if (!fs.existsSync(csvPath)) {
      runPythonInline(`from engine.citations import generate_citation_validation_report; generate_citation_validation_report()`);
    }
    res.setHeader('Content-Type', 'text/csv; charset=utf-8');
    res.setHeader('Content-Disposition', 'attachment; filename="incubrix_citation_targets_30.csv"');
    res.sendFile(csvPath);
  });

  app.get('/api/exports/coverage.csv', (_req: Request, res: Response) => {
    const csvPath = path.resolve(ROOT_DIR, 'exports/QUESTION_COVERAGE.csv');
    if (!fs.existsSync(csvPath)) {
      runPythonInline(`from engine.coverage import generate_question_coverage_report; generate_question_coverage_report()`);
    }
    res.setHeader('Content-Type', 'text/csv; charset=utf-8');
    res.setHeader('Content-Disposition', 'attachment; filename="incubrix_question_coverage_100.csv"');
    res.sendFile(csvPath);
  });

  app.get('/api/exports/workbook', (req: Request, res: Response) => {
    try {
      const bundlePath = path.resolve(ROOT_DIR, 'exports/workbook/assessment_workbook_bundle.json');
      if (!customDbPath && req.query.refresh !== 'true' && fs.existsSync(bundlePath)) {
        const cached = JSON.parse(fs.readFileSync(bundlePath, 'utf-8'));
        res.json(cached);
        return;
      }
      const bundle = runPythonInline(
        `import sys, json; from engine.reporting import export_assessment_workbook_bundle; db = sys.argv[1] if len(sys.argv) > 1 else None; print(json.dumps(export_assessment_workbook_bundle(db)))`,
        dbArgs
      );
      res.json(bundle);
    } catch (err: any) {
      res.status(500).json({ error: err.message });
    }
  });

  // Serve production frontend assets if dist/ exists (single-port hosting)
  const distDir = path.resolve(ROOT_DIR, 'dist');
  if (fs.existsSync(distDir)) {
    app.use(express.static(distDir));
    app.get('*', (req: Request, res: Response, next) => {
      if (req.path.startsWith('/api')) return next();
      const indexPath = path.join(distDir, 'index.html');
      if (fs.existsSync(indexPath)) {
        res.sendFile(indexPath);
      } else {
        next();
      }
    });
  }

  return app;
}

// Start server when executed directly
const isMain = process.argv[1] && path.resolve(process.argv[1]) === path.resolve(import.meta.filename);
if (isMain) {
  const port = Number(process.env.PORT || 3001);
  const app = createApp();
  app.listen(port, () => {
    console.log(`[IncuBrix API] Listening on http://localhost:${port}`);
  });
}
