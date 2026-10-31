import sqlite3
import json

conn = sqlite3.connect('data/incubrix.db')
c = conn.cursor()

# 1. Add evidence_tier and reference_metadata columns if not present
cols = [info[1] for info in c.execute('PRAGMA table_info(questions)').fetchall()]
if 'evidence_tier' not in cols:
    c.execute("ALTER TABLE questions ADD COLUMN evidence_tier TEXT DEFAULT 'AWAITING_MEASUREMENT'")
    print("Added evidence_tier to questions.")
if 'reference_metadata_json' not in cols:
    c.execute("ALTER TABLE questions ADD COLUMN reference_metadata_json TEXT DEFAULT '{}'")
    print("Added reference_metadata_json to questions.")

# 2. Get questions covered by content pages
content_qids = set()
for row in c.execute("SELECT target_question_ids_json, supporting_questions_json FROM content_pages").fetchall():
    if row[0]:
        try:
            content_qids.update(json.loads(row[0]))
        except:
            pass
    if row[1]:
        try:
            content_qids.update(json.loads(row[1]))
        except:
            pass

print(f"Questions referenced by Content Studio pages: {len(content_qids)}")

# 3. Get citation targets questions
citation_qids = set()
for row in c.execute("SELECT relevant_question_id FROM citation_opportunities WHERE relevant_question_id IS NOT NULL").fetchall():
    citation_qids.add(row[0])
print(f"Questions referenced by Citation targets: {len(citation_qids)}")

# 4. Check two-pass verified questions
obs_verified = set(r[0] for r in c.execute("""
    SELECT DISTINCT question_id FROM visibility_observations 
    WHERE collection_status = 'verified_observation' AND is_demo = 0
""").fetchall())

# 5. Check pending / partially measured questions
obs_pending = set(r[0] for r in c.execute("""
    SELECT DISTINCT question_id FROM visibility_observations 
    WHERE collection_status = 'pending_verification' AND is_demo = 0
""").fetchall()) - obs_verified

# 6. Check demo questions
obs_demo = set(r[0] for r in c.execute("""
    SELECT DISTINCT question_id FROM visibility_observations 
    WHERE is_demo = 1
""").fetchall()) - obs_verified - obs_pending

# Questions with genuine reference research from content studio or citations or first party faq
reference_qids = (content_qids | citation_qids) - obs_verified - obs_pending - obs_demo

print(f"GENUINE_VERIFIED: {len(obs_verified)} -> {sorted(list(obs_verified))}")
print(f"PARTIALLY_MEASURED: {len(obs_pending)} -> {sorted(list(obs_pending))}")
print(f"DEMO: {len(obs_demo)} -> {sorted(list(obs_demo))}")
print(f"REFERENCE_ONLY: {len(reference_qids)} -> {sorted(list(reference_qids))}")

# 7. Update all 100 questions in database
all_qs = c.execute("SELECT id, canonical_question, source_url, source_type FROM questions").fetchall()
awaiting_count = 0

for q in all_qs:
    qid, q_text, src_url, src_type = q
    if qid in obs_verified:
        tier = 'GENUINE_VERIFIED'
        meta = {
            "methodology": "Two-pass live API and standardized manual protocol across multiple providers",
            "passes_recorded": 2,
            "verification_status": "verified_concordant"
        }
    elif qid in obs_pending:
        tier = 'PARTIALLY_MEASURED'
        meta = {
            "methodology": "Single-pass baseline observation recorded; awaiting Pass 2 repeat verification",
            "passes_recorded": 1,
            "verification_status": "pending_repeat_pass"
        }
    elif qid in obs_demo:
        tier = 'DEMO'
        meta = {
            "methodology": "Offline simulation demonstration sandbox record",
            "passes_recorded": 1,
            "verification_status": "demo_simulation"
        }
    elif qid in reference_qids:
        tier = 'REFERENCE_ONLY'
        meta = {
            "methodology": "Editorial and competitor benchmark research derived from IncuBrix Content Studio guides, first-party documentation, and directory citations",
            "source_provenance": src_url,
            "verification_status": "offline_reference_benchmark"
        }
    else:
        tier = 'AWAITING_MEASUREMENT'
        awaiting_count += 1
        meta = {
            "methodology": "Validated creator query queued in priority pipeline awaiting provider API key or manual researcher hours",
            "source_provenance": src_url,
            "verification_status": "queued_unmeasured"
        }
    
    c.execute("UPDATE questions SET evidence_tier = ?, reference_metadata_json = ? WHERE id = ?", (tier, json.dumps(meta), qid))

conn.commit()

# Print summary counts
tiers = c.execute("SELECT evidence_tier, COUNT(*) FROM questions GROUP BY evidence_tier ORDER BY COUNT(*) DESC").fetchall()
print("\nFinal Questions by Evidence Tier:")
for t, cnt in tiers:
    print(f"  {t}: {cnt}")

conn.close()

