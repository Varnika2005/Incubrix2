import sqlite3

conn = sqlite3.connect('data/incubrix.db')
c = conn.cursor()

# Inspect all questions
qs = c.execute("SELECT id, canonical_question, category, search_intent, target_persona, source_url, source_type, priority_score FROM questions ORDER BY id").fetchall()
print(f"Total Questions: {len(qs)}")

# Inspect existing observations per question
obs_counts = c.execute("""
    SELECT question_id, 
           COUNT(*) as total_obs,
           SUM(CASE WHEN collection_status = 'verified_observation' THEN 1 ELSE 0 END) as verified_obs,
           SUM(CASE WHEN collection_status = 'pending_verification' THEN 1 ELSE 0 END) as pending_obs,
           SUM(CASE WHEN is_demo = 1 THEN 1 ELSE 0 END) as demo_obs
    FROM visibility_observations
    GROUP BY question_id
""").fetchall()

obs_map = {r[0]: {'total': r[1], 'verified': r[2], 'pending': r[3], 'demo': r[4]} for r in obs_counts}

verified_count = 0
partial_count = 0
demo_count = 0
no_obs_count = 0

for q in qs:
    qid = q[0]
    info = obs_map.get(qid, {'total': 0, 'verified': 0, 'pending': 0, 'demo': 0})
    if info['verified'] > 0:
        verified_count += 1
    elif info['pending'] > 0:
        partial_count += 1
    elif info['demo'] > 0:
        demo_count += 1
    else:
        no_obs_count += 1

print(f"Verified (2-pass): {verified_count}")
print(f"Partially measured: {partial_count}")
print(f"Demo only: {demo_count}")
print(f"No observations (queued): {no_obs_count}")
conn.close()

