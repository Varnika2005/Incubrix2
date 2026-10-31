import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import sqlite3, json, re
from engine.auditor import validate_json_ld

conn = sqlite3.connect('data/incubrix.db')
c = conn.cursor()

for pid in ['PAGE-004', 'PAGE-007', 'PAGE-008', 'PAGE-009', 'PAGE-010']:
    row = c.execute("SELECT page_id, slug, content_type, title, meta_description, direct_answer_summary, body_markdown, headings_json, citations_json, internal_links_json, json_ld_schema, unverified_claims_flagged_json, word_count, status FROM content_pages WHERE page_id = ?", (pid,)).fetchone()
    (page_id, slug, content_type, title, meta_description, direct_answer,
     body_md, headings_json, citations_json, links_json, json_ld,
     unverified_claims_json, word_count, status) = row

    intent_ok = bool(direct_answer and len(direct_answer.strip()) >= 50)
    aeo_ok = 'IncuBrix' in direct_answer and bool(re.search(r'(video|creator|podcast|clip|repurpose|pricing)', direct_answer, re.I))
    unverified_claims = json.loads(unverified_claims_json or '[]')
    claims_ok = len(unverified_claims) == 0 or all(c.get('resolved', False) for c in unverified_claims)
    citations = json.loads(citations_json or '[]')
    citations_ok = len(citations) >= 2
    title_len = len(title)
    meta_len = len(meta_description)
    title_ok = 30 <= title_len <= 90
    meta_ok = 80 <= meta_len <= 180
    headings = json.loads(headings_json or '[]')
    headings_ok = len(headings) >= 2
    words_ok = word_count >= 180
    links = json.loads(links_json or '[]')
    links_ok = len(links) >= 2
    faq_ok = '?' in body_md or content_type == 'faq_page' or 'FAQ' in body_md or len(headings) >= 3
    schema_ok, schema_errs = validate_json_ld(json_ld)
    dup_ok = True
    grammar_ok = not ('one content' in body_md or '||' in body_md)
    broken_links_ok = not ('http://localhost' in (links_json or '') or 'undefined' in (links_json or ''))
    stats_ok = True

    failures = []
    checks = {
        'intent_ok': intent_ok, 'aeo_ok': aeo_ok, 'claims_ok': claims_ok, 'citations_ok': citations_ok,
        'title_ok': title_ok, 'meta_ok': meta_ok, 'headings_ok': headings_ok, 'words_ok': words_ok,
        'links_ok': links_ok, 'faq_ok': faq_ok, 'schema_ok': schema_ok, 'dup_ok': dup_ok,
        'grammar_ok': grammar_ok, 'broken_links_ok': broken_links_ok, 'stats_ok': stats_ok
    }
    for k, v in checks.items():
        if not v:
            failures.append(k)
    print(f"{pid}: {failures}")
    if 'aeo_ok' in failures:
        print(f"  direct_answer: {direct_answer}")
    if 'meta_ok' in failures:
        print(f"  meta_len: {meta_len}, meta: {meta_description}")
    if 'title_ok' in failures:
        print(f"  title_len: {title_len}, title: {title}")

conn.close()
