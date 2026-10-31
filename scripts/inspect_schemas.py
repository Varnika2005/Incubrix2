import sqlite3

conn = sqlite3.connect('data/incubrix.db')
c = conn.cursor()

tables = ['questions', 'visibility_observations', 'technical_issues', 'content_pages', 'citation_opportunities']
for table in tables:
    print(f"\n=== SCHEMA FOR {table} ===")
    info = c.execute(f"PRAGMA table_info({table})").fetchall()
    for col in info:
        print(f"  {col[1]} ({col[2]})")

conn.close()

