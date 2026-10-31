import csv
import json
import os
import sqlite3

print("=================================================================")
print("=== REQUIREMENT 1: 100 REAL QUESTIONS MEASURED ===")
print("=================================================================")
with open('submission/reports/QUESTION_COVERAGE.csv', 'r', encoding='utf-8') as f:
    r_cov = list(csv.DictReader(f))

two_pass = [r for r in r_cov if r['coverage_status'] == 'two_pass_verified']
queued = [r for r in r_cov if r['coverage_status'] == 'queued_ready_for_collection']
print(f"Total rows in QUESTION_COVERAGE.csv: {len(r_cov)}")
print(f"Two-pass verified measured questions: {len(two_pass)}")
print(f"Queued ready for collection: {len(queued)}")
for tp in two_pass:
    print(f"  {tp['question_id']} (Obs: {tp['verified_observations_count']}, P1:{tp['pass1_count']}/P2:{tp['pass2_count']}, Providers: {tp['providers_measured']}, Markets: {tp['markets_measured']})")

print("\n=================================================================")
print("=== REQUIREMENT 2: FOUR AI ASSISTANTS GENUINELY CHECKED ===")
print("=================================================================")
conn = sqlite3.connect('data/incubrix.db')
c = conn.cursor()
providers_data = c.execute("""
    SELECT provider, 
           COUNT(*) as total_obs,
           SUM(CASE WHEN is_demo = 0 THEN 1 ELSE 0 END) as non_demo_obs,
           SUM(CASE WHEN collection_status = 'verified_observation' THEN 1 ELSE 0 END) as verified_obs,
           COUNT(DISTINCT question_id) as distinct_qs,
           GROUP_CONCAT(DISTINCT observation_date) as dates
    FROM visibility_observations
    WHERE is_demo = 0
    GROUP BY provider
""").fetchall()

for p in providers_data:
    print(f"Provider: {p[0].upper()}")
    print(f"  Non-demo obs: {p[2]} (Verified: {p[3]})")
    print(f"  Distinct questions: {p[4]}")
    print(f"  Dates: {p[5]}")

print("\n=================================================================")
print("=== REQUIREMENT 3: TWO MEASUREMENT DAYS ===")
print("=================================================================")
dates_data = c.execute("""
    SELECT observation_date, 
           COUNT(*) as obs_count,
           COUNT(DISTINCT question_id) as q_count,
           GROUP_CONCAT(DISTINCT provider) as providers,
           GROUP_CONCAT(DISTINCT market) as markets
    FROM visibility_observations
    WHERE is_demo = 0 AND collection_status = 'verified_observation'
    GROUP BY observation_date
    ORDER BY observation_date
""").fetchall()

for d in dates_data:
    print(f"Date {d[0]}: {d[1]} verified obs across {d[2]} questions | Providers: {d[3]} | Markets: {d[4]}")

print("\n=================================================================")
print("=== REQUIREMENT 4: 20 VALIDATED TECHNICAL FIXES WITH VALIDATOR EVIDENCE ===")
print("=================================================================")
tech_fixes = c.execute("""
    SELECT issue_id, severity, priority_rank, page_url, title, validation_method, validation_status, validation_result
    FROM technical_issues
    ORDER BY priority_rank ASC
""").fetchall()
print(f"Total Technical Issues in DB: {len(tech_fixes)}")
for tf in tech_fixes:
    print(f"  [{tf[0]}] Rank {tf[2]} | {tf[1].upper()} | Status: {tf[6]} | Method: {tf[5]}")

print("\n=================================================================")
print("=== REQUIREMENT 5: 10 PUBLISH-READY CONTENT PAGES ===")
print("=================================================================")
pages = c.execute("""
    SELECT page_id, slug, content_type, word_count, status, title
    FROM content_pages
    ORDER BY page_id ASC
""").fetchall()
print(f"Total Content Pages in DB: {len(pages)}")
for pg in pages:
    print(f"  [{pg[0]}] {pg[1]} | Type: {pg[2]} | Words: {pg[3]} | Status: {pg[4]}")

print("\n=================================================================")
print("=== REQUIREMENT 6: 30 CITATION TARGETS ===")
print("=================================================================")
with open('submission/citation_plan/CITATION_TARGETS.csv', 'r', encoding='utf-8') as f:
    cit_targets = list(csv.DictReader(f))
print(f"Total Citation Targets in CSV: {len(cit_targets)}")
h200 = [t for t in cit_targets if t['http_status_checked'] == '200']
h403 = [t for t in cit_targets if t['http_status_checked'] == '403']
avg_score = sum(float(t['quality_score']) for t in cit_targets) / len(cit_targets)
print(f"HTTP 200: {len(h200)} targets")
print(f"HTTP 403 (WAF): {len(h403)} targets")
print(f"Average Quality Score: {avg_score:.1f}/100")

conn.close()
