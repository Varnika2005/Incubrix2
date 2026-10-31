import csv
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from engine.auditor import (
    get_prioritized_technical_issues,
    parse_html_signals,
    run_live_website_audit,
    validate_json_ld,
    validate_single_issue_patch,
)
from engine.citations import export_citations_to_csv, seed_citation_opportunities
from engine.content_studio import (
    TEN_PUBLISH_READY_PAGES,
    export_content_page_files,
    generate_content_brief,
    seed_content_pages,
    validate_content_page,
)
from engine.db import get_connection, init_schema
from engine.questions_seed import (
    RAW_CREATOR_QUESTIONS,
    deduplicate_questions,
    export_questions_to_csv,
    import_questions_from_csv,
    normalize_question_fingerprint,
    seed_questions,
    validate_question_record,
)
from engine.reporting import (
    compute_overview_metrics,
    export_assessment_workbook_bundle,
    generate_weekly_report,
    seed_launch_plan,
)
from engine.visibility import (
    call_live_provider_adapter,
    compare_observations_across_dates,
    execute_visibility_run,
    export_visibility_to_csv,
    extract_visibility_signals,
    record_manual_observation,
    seed_baseline_visibility_observations,
)


class TestIncuBrixEngineSuite(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = str(Path(self.temp_dir.name) / "test_incubrix.db")
        init_schema(self.db_path)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    # 1. Question Deduplication & 2. Source Provenance
    def test_question_deduplication_preserves_provenance(self) -> None:
        raw_sample = [
            {
                "id": "Q-001",
                "canonical_question": "What is the best AI studio to turn one recording into a full week of creator content?",
                "original_wording": "best AI studio to turn one recording into a week of content",
                "category": "Content Creation",
                "search_intent": "commercial",
                "target_persona": "Creator",
                "source_url": "https://incubrix.com/investors",
                "source_type": "first_party_faq",
                "collection_date": "2026-10-20",
                "priority_score": 90,
            },
            {
                "id": "Q-DUP",
                "canonical_question": "What is the best AI studio to turn one recording into a full week of creator content!",
                "original_wording": "Which AI studio turns one recording into a full week of creator content?",
                "category": "Content Creation",
                "search_intent": "commercial",
                "target_persona": "Creator",
                "source_url": "https://www.reddit.com/r/NewTubers/",
                "source_type": "public_community",
                "collection_date": "2026-10-21",
                "priority_score": 98,
            },
        ]
        deduped = deduplicate_questions(raw_sample)
        self.assertEqual(len(deduped), 1)
        merged = deduped[0]
        self.assertEqual(merged["duplicate_merge_count"], 1)
        self.assertEqual(merged["priority_score"], 98)
        self.assertEqual(len(merged["provenance_sources"]), 2)
        urls = [p["source_url"] for p in merged["provenance_sources"]]
        self.assertIn("https://incubrix.com/investors", urls)
        self.assertIn("https://www.reddit.com/r/NewTubers/", urls)

        # Verify full 100 creator questions seed
        seed_res = seed_questions(self.db_path)
        self.assertEqual(seed_res["unique_validated_count"], 100)
        self.assertGreaterEqual(seed_res["duplicates_merged_preserving_provenance"], 6)

    # 3. Visibility Calculations & DEMO Exclusion + Two-Pass AI Rule
    def test_visibility_calculations_and_two_pass_verification(self) -> None:
        seed_questions(self.db_path)
        seed_baseline_visibility_observations(self.db_path)

        # Test manual observation: Pass 1 on Q-002 should be 'pending_verification'
        obs_p1 = record_manual_observation(
            {
                "question_id": "Q-002",
                "provider": "chatgpt",
                "market": "US",
                "observation_date": "2026-10-24",
                "pass_number": 1,
                "raw_response_text": "Creators use IncuBrix Content Insights (https://incubrix.com/) and VidIQ to find trending niche topics.",
                "citation_urls": ["https://incubrix.com/"],
            },
            self.db_path,
        )
        self.assertEqual(obs_p1["collection_status"], "pending_verification")
        self.assertEqual(obs_p1["incubrix_mentioned"], 1)
        self.assertEqual(obs_p1["incubrix_cited"], 1)

        # Now record Pass 2 on Q-002 -> both Pass 1 and Pass 2 become 'verified_observation'!
        obs_p2 = record_manual_observation(
            {
                "question_id": "Q-002",
                "provider": "chatgpt",
                "market": "US",
                "observation_date": "2026-10-24",
                "pass_number": 2,
                "raw_response_text": "Pass 2: IncuBrix (https://incubrix.com/how-it-works) scans trending topics and competitor gaps alongside TubeBuddy.",
                "citation_urls": ["https://incubrix.com/how-it-works"],
            },
            self.db_path,
        )
        self.assertEqual(obs_p2["collection_status"], "verified_observation")

        # Record a single-pass observation on Q-003 -> must remain 'pending_verification' and NOT count in verified AI rate
        obs_single = record_manual_observation(
            {
                "question_id": "Q-003",
                "provider": "claude",
                "market": "US",
                "observation_date": "2026-10-24",
                "pass_number": 1,
                "raw_response_text": "Single pass test mentioning IncuBrix (https://incubrix.com/).",
                "citation_urls": ["https://incubrix.com/"],
            },
            self.db_path,
        )
        self.assertEqual(obs_single["collection_status"], "pending_verification")

        metrics = compute_overview_metrics(self.db_path)
        # Ensure DEMO records exist in state breakdown but are excluded from AI mention/citation totals
        self.assertGreater(metrics["observation_states"]["demo_observation"], 0)
        self.assertGreater(metrics["observation_states"]["verified_observation"], 0)
        self.assertGreaterEqual(metrics["observation_states"]["pending_verification"], 1)
        self.assertGreater(metrics["ai_visibility"]["mention_rate_pct"], 0)

    # 4. Missing Credentials, Timeouts, HTTP 429, Malformed JSON, and Empty Datasets
    def test_missing_failed_observations_and_provider_edge_cases(self) -> None:
        seed_questions(self.db_path)
        seed_baseline_visibility_observations(self.db_path)
        metrics = compute_overview_metrics(self.db_path)
        self.assertGreater(metrics["observation_states"]["not_collected"], 0)
        self.assertGreater(metrics["observation_states"]["failed_collection"], 0)

        # 4a. Missing credentials -> returns 'not_collected'
        with patch.dict("os.environ", {"OPENAI_API_KEY": ""}, clear=False):
            res_missing = call_live_provider_adapter("chatgpt", "What is CreatorOps?", "US")
            self.assertFalse(res_missing["ok"])
            self.assertEqual(res_missing["status"], "not_collected")

        # 4b. Network timeout -> returns 'failed_collection'
        with patch.dict("os.environ", {"OPENAI_API_KEY": "sk-test-fake-key-for-timeout"}):
            with patch("urllib.request.urlopen", side_effect=TimeoutError("Simulated socket timeout after 15s")):
                res = call_live_provider_adapter("chatgpt", "What is CreatorOps?", "US", timeout_sec=1, max_retries=1)
                self.assertFalse(res["ok"])
                self.assertEqual(res["status"], "failed_collection")
                self.assertIn("TimeoutError", res["error"])

        # 4c. HTTP 429 Rate Limit -> returns 'failed_collection' with HTTP 429 message
        import urllib.error
        import io
        http_429 = urllib.error.HTTPError(
            url="https://api.openai.com/v1/chat/completions",
            code=429,
            msg="Too Many Requests",
            hdrs=None,  # type: ignore
            fp=io.BytesIO(b'{"error": "Rate limit exceeded"}'),
        )
        with patch.dict("os.environ", {"OPENAI_API_KEY": "sk-test-fake-key-429"}):
            with patch("urllib.request.urlopen", side_effect=http_429):
                res_429 = call_live_provider_adapter("chatgpt", "What is CreatorOps?", "US", timeout_sec=1, max_retries=0)
                self.assertFalse(res_429["ok"])
                self.assertEqual(res_429["status"], "failed_collection")
                self.assertIn("429", res_429["error"])

        # 4d. Malformed JSON response -> returns 'failed_collection' with MalformedJSONError
        class DummyResp:
            def __init__(self, payload: bytes) -> None:
                self.payload = payload
            def read(self) -> bytes:
                return self.payload
            def __enter__(self):
                return self
            def __exit__(self, *args):
                pass

        with patch.dict("os.environ", {"OPENAI_API_KEY": "sk-test-fake-key-malformed"}):
            with patch("urllib.request.urlopen", return_value=DummyResp(b"NOT_VALID_JSON{{{")):
                res_mal = call_live_provider_adapter("chatgpt", "What is CreatorOps?", "US", timeout_sec=1, max_retries=0)
                self.assertFalse(res_mal["ok"])
                self.assertEqual(res_mal["status"], "failed_collection")
                self.assertIn("MalformedJSONError", res_mal["error"])

        # 4e. Empty dataset / empty choices -> returns 'failed_collection' with EmptyResponseError
        with patch.dict("os.environ", {"OPENAI_API_KEY": "sk-test-fake-key-empty"}):
            with patch("urllib.request.urlopen", return_value=DummyResp(b'{"choices": [{"message": {"content": "   "}}]}')):
                res_empty = call_live_provider_adapter("chatgpt", "What is CreatorOps?", "US", timeout_sec=1, max_retries=0)
                self.assertFalse(res_empty["ok"])
                self.assertEqual(res_empty["status"], "failed_collection")
                self.assertIn("EmptyResponseError", res_empty["error"])

    # 5. Multi-Date Comparisons & Idempotent Rerun Duplicate/Promotion Prevention
    def test_multi_date_comparisons_and_idempotent_rerun(self) -> None:
        seed_questions(self.db_path)
        seed_baseline_visibility_observations(self.db_path)

        # Record verified 2-pass observations on 2026-10-22 and 2026-10-24 for Q-001
        for p in (1, 2):
            record_manual_observation(
                {
                    "question_id": "Q-001",
                    "provider": "chatgpt",
                    "market": "US",
                    "observation_date": "2026-10-22",
                    "pass_number": p,
                    "raw_response_text": "Day 1: IncuBrix is a CreatorOps platform.",
                    "citation_urls": [],
                },
                self.db_path,
            )
            record_manual_observation(
                {
                    "question_id": "Q-001",
                    "provider": "chatgpt",
                    "market": "US",
                    "observation_date": "2026-10-24",
                    "pass_number": p,
                    "raw_response_text": "Day 2: IncuBrix (https://incubrix.com/) is a CreatorOps platform.",
                    "citation_urls": ["https://incubrix.com/"],
                },
                self.db_path,
            )

        comp = compare_observations_across_dates("2026-10-22", "2026-10-24", self.db_path)
        self.assertTrue(comp["two_day_measurement_exists"])
        self.assertGreaterEqual(comp["paired_two_day_comparisons_count"], 1)
        self.assertGreaterEqual(comp["gained_citations"], 1)

        # Test idempotent rerun does not duplicate rows AND does not falsely promote failed/pending rows to verified
        conn = get_connection(self.db_path)
        before_cnt = conn.execute("SELECT COUNT(*) AS c FROM visibility_observations").fetchone()["c"]
        before_failed = conn.execute(
            "SELECT COUNT(*) AS c FROM visibility_observations WHERE collection_status = 'failed_collection'"
        ).fetchone()["c"]
        conn.close()

        execute_visibility_run(
            mode="test",
            markets=["US"],
            providers=["google_search"],
            limit=3,
            observation_date="2026-10-24",
            pass_number=1,
            custom_db_path=self.db_path,
        )
        conn = get_connection(self.db_path)
        after_first_run = conn.execute("SELECT COUNT(*) AS c FROM visibility_observations").fetchone()["c"]
        conn.close()

        # Run exact same parameters a second time -> row count and failed count must remain identical!
        execute_visibility_run(
            mode="test",
            markets=["US"],
            providers=["google_search"],
            limit=3,
            observation_date="2026-10-24",
            pass_number=1,
            custom_db_path=self.db_path,
        )
        conn = get_connection(self.db_path)
        after_second_run = conn.execute("SELECT COUNT(*) AS c FROM visibility_observations").fetchone()["c"]
        after_failed = conn.execute(
            "SELECT COUNT(*) AS c FROM visibility_observations WHERE collection_status = 'failed_collection'"
        ).fetchone()["c"]
        conn.close()
        self.assertEqual(after_first_run, after_second_run)
        self.assertEqual(before_failed, after_failed)

    # 6. CSV Import and Export
    def test_csv_import_and_export(self) -> None:
        seed_questions(self.db_path)
        seed_baseline_visibility_observations(self.db_path)

        q_csv = Path(self.temp_dir.name) / "questions.csv"
        v_csv = Path(self.temp_dir.name) / "visibility.csv"

        q_rows = export_questions_to_csv(q_csv, self.db_path)
        v_rows = export_visibility_to_csv(v_csv, include_demo=False, custom_db_path=self.db_path)
        self.assertEqual(q_rows, 100)
        self.assertGreater(v_rows, 10)

        # Import back into the same DB -> all 100 should merge cleanly without creating duplicate rows
        imp_res = import_questions_from_csv(q_csv, self.db_path)
        self.assertEqual(imp_res["imported_new"], 0)
        self.assertEqual(imp_res["merged_existing"], 100)

    # 7. Technical Audit Rules & 8. Structured-Data Validation (Live vs Candidate Patch)
    def test_technical_audit_rules_and_json_ld_validation(self) -> None:
        sample_html = """
        <!DOCTYPE html>
        <html>
        <head>
          <title>IncuBrix Test Page</title>
          <meta name="description" content="Sample description for testing parser signals.">
          <link rel="canonical" href="https://incubrix.com/test">
        </head>
        <body>
          <h1></h1>
          <h2>Section One</h2>
          <img src="/a.jpg" alt="">
          <img src="/b.jpg" alt="Valid alt description">
          <a href="/pricing">Pricing</a>
        </body>
        </html>
        """
        signals = parse_html_signals(sample_html, "https://incubrix.com/test")
        self.assertEqual(signals["title"], "IncuBrix Test Page")
        self.assertEqual(signals["h1_tags"], [""])
        self.assertEqual(signals["images_total"], 2)
        self.assertEqual(signals["images_missing_alt"], 1)
        self.assertEqual(len(signals["json_ld_blocks"]), 0)

        # Test JSON-LD validation rejects fabricated AggregateRating / review
        fake_rating_schema = json.dumps(
            {
                "@context": "https://schema.org",
                "@type": "SoftwareApplication",
                "name": "IncuBrix",
                "applicationCategory": "MultimediaApplication",
                "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.9", "reviewCount": "500"},
            }
        )
        ok, errs = validate_json_ld(fake_rating_schema)
        self.assertFalse(ok)
        self.assertTrue(any("prohibited unverified schema property" in e.lower() for e in errs))

        # Verify all 22 prioritized technical fixes pass candidate patch validation while live_fixes_validated == 0
        audit_res = run_live_website_audit(fetch_live=False, validate_patches=True, custom_db_path=self.db_path)
        self.assertEqual(audit_res["issues_total"], 22)
        self.assertEqual(audit_res["live_fixes_validated"], 0)
        self.assertEqual(audit_res["patch_artifacts_validated"], 22)

    # 9. Content Validation Checks & 10. Report Generation
    def test_content_studio_validation_and_report_generation(self) -> None:
        seed_questions(self.db_path)
        seed_baseline_visibility_observations(self.db_path)
        run_live_website_audit(fetch_live=False, validate_patches=True, custom_db_path=self.db_path)
        cs_res = seed_content_pages(self.db_path)
        self.assertEqual(cs_res["content_pages_seeded"], 10)
        self.assertEqual(cs_res["all_passed_validation"], True)

        # Verify that marking a page with unverified_claims_flagged as 'ready_to_publish' fails validation
        bad_page = dict(TEN_PUBLISH_READY_PAGES[0])
        bad_page["status"] = "ready_to_publish"
        bad_page["unverified_claims_flagged"] = ["Unverified roadmap claim"]
        ok_page, page_errs = validate_content_page(bad_page)
        self.assertFalse(ok_page)
        self.assertTrue(any("cannot be marked 'ready_to_publish'" in e for e in page_errs))

        seed_citation_opportunities(self.db_path, fetch_live=False)
        seed_launch_plan(self.db_path)

        # Test brief generator
        brief = generate_content_brief("Q-001", "how_to_guide", self.db_path)
        self.assertEqual(brief["question_id"], "Q-001")
        self.assertIn("IncuBrix", brief["direct_answer_draft"])

        # Test report generation & workbook export
        rep = generate_weekly_report(self.db_path)
        self.assertIn("IncuBrix Weekly AEO / SEO / GEO Visibility Report", rep["report_markdown"])
        wb = export_assessment_workbook_bundle(self.db_path)
        for k, passed in wb["completeness_verification"].items():
            self.assertTrue(passed, f"Workbook completeness check {k} failed")

    # 11. Citation Validation & Quality Scoring
    def test_citation_quality_scoring_and_report(self) -> None:
        from engine.citations import calculate_citation_quality_score, generate_citation_validation_report
        seed_citation_opportunities(self.db_path, fetch_live=False)
        rep_md = generate_citation_validation_report(self.db_path)
        self.assertIn("IncuBrix 30-Target Citation Opportunity & Validation Report", rep_md)
        self.assertIn("Quality Scoring Methodology", rep_md)

        # Verify quality score ranges
        sample_item = {
            "priority_tier": "Tier 1",
            "source_type": "directory",
            "http_status_checked": 200,
            "page_url": "https://www.producthunt.com/categories/video-editing",
        }
        score = calculate_citation_quality_score(sample_item)
        self.assertEqual(score, 100)

        sample_403 = {
            "priority_tier": "Tier 1",
            "source_type": "directory",
            "http_status_checked": 403,
            "page_url": "https://www.g2.com/categories/ai-video-generator",
        }
        score_403 = calculate_citation_quality_score(sample_403)
        self.assertEqual(score_403, 95)

    # 12. Local Technical Implementations (llms.txt, robots.txt, sitemap.xml)
    def test_local_technical_implementations(self) -> None:
        llms_path = Path("public/llms.txt")
        robots_path = Path("public/robots.txt")
        sitemap_path = Path("public/sitemap.xml")

        self.assertTrue(llms_path.exists(), "public/llms.txt must exist")
        self.assertTrue(robots_path.exists(), "public/robots.txt must exist")
        self.assertTrue(sitemap_path.exists(), "public/sitemap.xml must exist")

        llms_content = llms_path.read_text(encoding="utf-8")
        self.assertIn("IncuBrix", llms_content)
        self.assertIn("CreatorOps", llms_content)

        robots_content = robots_path.read_text(encoding="utf-8")
        self.assertIn("GPTBot", robots_content)
        self.assertIn("ClaudeBot", robots_content)
        self.assertIn("PerplexityBot", robots_content)



if __name__ == "__main__":
    unittest.main()
