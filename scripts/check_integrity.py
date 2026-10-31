import sqlite3

conn = sqlite3.connect('data/incubrix.db')
c = conn.cursor()

# Check foreign key violations
c.execute("PRAGMA foreign_key_check")
fk_errors = c.fetchall()
print(f"Foreign Key Violations: {len(fk_errors)}")

# Check question references in visibility_observations
orphan_obs = c.execute("""
    SELECT COUNT(*) FROM visibility_observations vo 
    LEFT JOIN questions q ON vo.question_id = q.id 
    WHERE q.id IS NULL
""").fetchone()[0]
print(f"Orphan observations: {orphan_obs}")

# Check content_pages references
orphan_cp = c.execute("""
    SELECT COUNT(*) FROM content_pages cp 
    WHERE cp.target_question_ids_json IS NULL OR cp.target_question_ids_json = '[]'
""").fetchone()[0]
print(f"Content pages without target questions: {orphan_cp}")

# Check secrets in db text fields
import re
key_pattern = re.compile(r'sk-[a-zA-Z0-9_-]{20,}')
c.execute("SELECT observation_id, response_snippet, raw_evidence_path FROM visibility_observations")
secret_leaks = 0
for row in c.fetchall():
    for text in row:
        if text and key_pattern.search(str(text)):
            secret_leaks += 1
print(f"Secret leaks in visibility_observations: {secret_leaks}")

conn.close()

