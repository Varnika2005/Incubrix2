import sqlite3
import json

conn = sqlite3.connect('data/incubrix.db')
c = conn.cursor()

# Check question observations
rows = c.execute("""
    SELECT q.id, q.canonical_question, q.category, q.validation_status,
           COUNT(vo.observation_id) as total_obs,
           SUM(CASE WHEN vo.collection_status = 'verified_observation' AND vo.is_demo = 0 THEN 1 ELSE 0 END) as verified_obs,
           SUM(CASE WHEN vo.is_demo = 1 THEN 1 ELSE 0 END) as demo_obs,
           SUM(CASE WHEN vo.collection_status = 'pending_verification' AND vo.is_demo = 0 THEN 1 ELSE 0 END) as pending_obs,
           SUM(CASE WHEN vo.collection_status IN ('not_collected', 'failed_collection') AND vo.is_demo = 0 THEN 1 ELSE 0 END) as uncollected_obs
    FROM questions q
    LEFT JOIN visibility_observations vo ON q.id = vo.question_id
    GROUP BY q.id
    ORDER BY q.id
""").fetchall()

print(f"Total Questions: {len(rows)}")
verified_qs = [r for r in rows if r[5] and r[5] > 0]
demo_qs = [r for r in rows if r[6] and r[6] > 0 and (not r[5] or r[5] == 0)]
pending_qs = [r for r in rows if r[7] and r[7] > 0 and (not r[5] or r[5] == 0)]
uncollected_qs = [r for r in rows if r[8] and r[8] > 0 and (not r[5] or r[5] == 0)]
zero_obs_qs = [r for r in rows if r[4] == 0]

print(f"Questions with verified obs: {len(verified_qs)}")
print(f"Questions with pending/partial obs: {len(pending_qs)}")
print(f"Questions with uncollected/failed test runs: {len(uncollected_qs)}")
print(f"Questions with demo obs only: {len(demo_qs)}")
print(f"Questions with zero obs records: {len(zero_obs_qs)}")

conn.close()

