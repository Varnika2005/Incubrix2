import sqlite3
import json

conn = sqlite3.connect('data/incubrix.db')
c = conn.cursor()

print("=== 1. QUESTIONS AUDIT ===")
total_q = c.execute("SELECT COUNT(*) FROM questions").fetchone()[0]
demo_q = c.execute("SELECT COUNT(*) FROM questions WHERE is_demo = 1").fetchone()[0]
non_demo_q = c.execute("SELECT COUNT(*) FROM questions WHERE is_demo = 0").fetchone()[0]
print(f"Total Questions: {total_q} (Real/Non-demo: {non_demo_q}, Demo: {demo_q})")

sample_q = c.execute("SELECT id, canonical_question, category, search_intent, target_persona, source_url FROM questions LIMIT 3").fetchall()
for q in sample_q:
    print(f"  {q[0]}: {q[1]} | {q[2]} | {q[3]} | {q[4]}")

print("\n=== 2. OBSERVATIONS AUDIT ===")
total_obs = c.execute("SELECT COUNT(*) FROM visibility_observations").fetchone()[0]
real_obs = c.execute("SELECT COUNT(*) FROM visibility_observations WHERE is_demo = 0").fetchone()[0]
demo_obs = c.execute("SELECT COUNT(*) FROM visibility_observations WHERE is_demo = 1").fetchone()[0]
print(f"Total Observations: {total_obs} (Real: {real_obs}, Demo: {demo_obs})")

distinct_q_measured = c.execute("SELECT COUNT(DISTINCT question_id) FROM visibility_observations WHERE is_demo = 0").fetchone()[0]
print(f"Distinct Questions Measured (Real): {distinct_q_measured} / 100")
measured_q_ids = [r[0] for r in c.execute("SELECT DISTINCT question_id FROM visibility_observations WHERE is_demo = 0 ORDER BY question_id").fetchall()]
print(f"Measured Question IDs: {measured_q_ids}")

print("\nBy Provider (Real):")
for p in c.execute("SELECT provider, COUNT(*), COUNT(DISTINCT question_id) FROM visibility_observations WHERE is_demo = 0 GROUP BY provider").fetchall():
    print(f"  {p[0]}: {p[1]} observations across {p[2]} distinct questions")

print("\nBy Date (Real):")
for d in c.execute("SELECT observation_date, COUNT(*), COUNT(DISTINCT question_id) FROM visibility_observations WHERE is_demo = 0 GROUP BY observation_date ORDER BY observation_date").fetchall():
    print(f"  {d[0]}: {d[1]} observations across {d[2]} distinct questions")

print("\nBy Collection Status:")
for s in c.execute("SELECT collection_status, is_demo, COUNT(*) FROM visibility_observations GROUP BY collection_status, is_demo").fetchall():
    print(f"  status={s[0]}, is_demo={s[1]}: {s[2]} observations")

print("\n=== 3. TECHNICAL ISSUES AUDIT ===")
total_tech = c.execute("SELECT COUNT(*) FROM technical_issues").fetchone()[0]
print(f"Total Technical Issues: {total_tech}")
for st in c.execute("SELECT validation_status, severity, COUNT(*) FROM technical_issues GROUP BY validation_status, severity").fetchall():
    print(f"  validation_status={st[0]}, severity={st[1]}: {st[2]}")

print("\n=== 4. CONTENT PAGES AUDIT ===")
total_cp = c.execute("SELECT COUNT(*) FROM content_pages").fetchone()[0]
print(f"Total Content Pages: {total_cp}")
for cp in c.execute("SELECT page_id, slug, status, word_count FROM content_pages").fetchall():
    print(f"  {cp[0]} ({cp[1]}): status={cp[2]}, words={cp[3]}")

print("\n=== 5. CITATION OPPORTUNITIES AUDIT ===")
total_cit = c.execute("SELECT COUNT(*) FROM citation_opportunities").fetchone()[0]
print(f"Total Citation Targets: {total_cit}")
for cit in c.execute("SELECT http_status_checked, verification_status, COUNT(*) FROM citation_opportunities GROUP BY http_status_checked, verification_status").fetchall():
    print(f"  http_status={cit[0]}, verification_status={cit[1]}: {cit[2]}")

conn.close()
