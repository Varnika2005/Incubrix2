import argparse
import json
import sys
from pathlib import Path

from engine.auditor import run_live_website_audit
from engine.citations import export_citations_to_csv, seed_citation_opportunities
from engine.content_studio import (
    TEN_PUBLISH_READY_PAGES,
    export_content_page_files,
    generate_content_brief,
    seed_content_pages,
)
from engine.db import EXPORTS_DIR, init_schema
from engine.questions_seed import export_questions_to_csv, seed_questions
from engine.reporting import (
    compute_overview_metrics,
    export_assessment_workbook_bundle,
    generate_weekly_report,
    seed_launch_plan,
)
from engine.visibility import (
    check_provider_Statuses,
    compare_observations_across_dates,
    execute_visibility_run,
    export_visibility_to_csv,
    seed_baseline_visibility_observations,
)
from engine.workbook_exporter import (
    generate_official_visibility_csv,
    populate_and_save_submission_workbook,
    SUBMISSION_DIR,
)


def cmd_init(args: argparse.Namespace) -> None:
    db_path = args.db
    init_schema(db_path)
    q_res = seed_questions(db_path)
    vis_res = seed_baseline_visibility_observations(db_path)
    audit_res = run_live_website_audit(
        target_url=args.target,
        fetch_live=args.live_audit,
        validate_patches=True,
        custom_db_path=db_path,
    )
    cs_res = seed_content_pages(db_path)
    for p in TEN_PUBLISH_READY_PAGES:
        export_content_page_files(p["page_id"], db_path)
    cit_res = seed_citation_opportunities(db_path, fetch_live=args.live_audit)
    lp_res = seed_launch_plan(db_path)
    rep_res = generate_weekly_report(db_path)

    export_visibility_to_csv(EXPORTS_DIR / "visibility_observations.csv", include_demo=False, custom_db_path=db_path)
    generate_official_visibility_csv(EXPORTS_DIR / "visibility.csv", custom_db_path=db_path)
    export_questions_to_csv(EXPORTS_DIR / "creator_questions_100.csv", custom_db_path=db_path)
    export_citations_to_csv(EXPORTS_DIR / "citation_opportunities_30.csv", custom_db_path=db_path)
    wb_res = export_assessment_workbook_bundle(db_path)
    populate_and_save_submission_workbook(EXPORTS_DIR / "workbook" / "IncuBrix_2027_Growth_Engineer_Option_3_AEO_SEO_GEO_Submission_Workbook.xlsx", custom_db_path=db_path)
    populate_and_save_submission_workbook(SUBMISSION_DIR / "workbook" / "IncuBrix_2027_Growth_Engineer_Option_3_AEO_SEO_GEO_Submission_Workbook.xlsx", custom_db_path=db_path)

    summary = {
        "status": "initialized",
        "questions": q_res,
        "baseline_visibility": vis_res,
        "technical_audit": {
            "pages_crawled": audit_res["pages_crawled"],
            "issues_total": audit_res["issues_total"],
            "live_fixes_validated": audit_res.get("live_fixes_validated", 0),
            "patch_artifacts_validated": audit_res.get("patch_artifacts_validated", audit_res["fixes_validated"]),
            "fixes_validated": audit_res["fixes_validated"],
        },
        "content_studio": cs_res,
        "citations": cit_res,
        "launch_plan": lp_res,
        "weekly_report_id": rep_res["report_id"],
        "workbook_completeness": wb_res["completeness_verification"],
    }
    print(json.dumps(summary, indent=2))


def cmd_audit(args: argparse.Namespace) -> None:
    init_schema(args.db)
    res = run_live_website_audit(
        target_url=args.target,
        fetch_live=not args.cached,
        validate_patches=True,
        custom_db_path=args.db,
    )
    print(json.dumps(res, indent=2))


def cmd_run_visibility(args: argparse.Namespace) -> None:
    init_schema(args.db)
    markets = [m.strip() for m in args.markets.split(",") if m.strip()]
    providers = [p.strip() for p in args.providers.split(",") if p.strip()]
    res = execute_visibility_run(
        mode=args.mode,
        markets=markets,
        providers=providers,
        limit=args.limit,
        observation_date=args.date,
        pass_number=args.pass_number,
        custom_db_path=args.db,
    )
    export_visibility_to_csv(EXPORTS_DIR / "visibility_observations.csv", include_demo=False, custom_db_path=args.db)
    print(json.dumps(res, indent=2))


def cmd_generate_brief(args: argparse.Namespace) -> None:
    init_schema(args.db)
    res = generate_content_brief(args.question_id, args.content_type, custom_db_path=args.db)
    print(json.dumps(res, indent=2))


def cmd_generate_report(args: argparse.Namespace) -> None:
    init_schema(args.db)
    res = generate_weekly_report(custom_db_path=args.db)
    print(
        json.dumps(
            {
                "report_id": res["report_id"],
                "report_path": res["report_path"],
                "generated_at": res["generated_at"],
            },
            indent=2,
        )
    )


def cmd_export_all(args: argparse.Namespace) -> None:
    init_schema(args.db)
    obs_cnt = export_visibility_to_csv(EXPORTS_DIR / "visibility_observations.csv", include_demo=False, custom_db_path=args.db)
    vis_cnt = generate_official_visibility_csv(EXPORTS_DIR / "visibility.csv", custom_db_path=args.db)
    q_cnt = export_questions_to_csv(EXPORTS_DIR / "creator_questions_100.csv", custom_db_path=args.db)
    cit_cnt = export_citations_to_csv(EXPORTS_DIR / "citation_opportunities_30.csv", custom_db_path=args.db)
    wb = export_assessment_workbook_bundle(custom_db_path=args.db)
    wb_file = populate_and_save_submission_workbook(EXPORTS_DIR / "workbook" / "IncuBrix_2027_Growth_Engineer_Option_3_AEO_SEO_GEO_Submission_Workbook.xlsx", custom_db_path=args.db)
    populate_and_save_submission_workbook(SUBMISSION_DIR / "workbook" / "IncuBrix_2027_Growth_Engineer_Option_3_AEO_SEO_GEO_Submission_Workbook.xlsx", custom_db_path=args.db)
    print(
        json.dumps(
            {
                "visibility_csv_rows": vis_cnt,
                "visibility_observations_rows": obs_cnt,
                "questions_csv_rows": q_cnt,
                "citations_csv_rows": cit_cnt,
                "workbook_bundle": wb,
                "submission_workbook": wb_file,
            },
            indent=2,
        )
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m engine.cli",
        description="IncuBrix AEO / SEO / GEO Visibility Engine CLI",
    )
    parser.add_argument("--db", default=None, help="Optional custom SQLite database path")
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="Initialize database, questions, live audit, content, citations, and reports")
    p_init.add_argument("--target", default="https://www.incubrix.com", help="Target website URL")
    p_init.add_argument("--live-audit", action="store_true", default=True, help="Crawl live incubrix.com pages")
    p_init.add_argument("--no-live-audit", action="store_false", dest="live_audit", help="Skip live HTTP crawl")
    p_init.set_defaults(func=cmd_init)

    p_audit = sub.add_parser("audit", help="Run Technical SEO, AEO & GEO website audit")
    p_audit.add_argument("--target", default="https://www.incubrix.com", help="Target website URL")
    p_audit.add_argument("--cached", action="store_true", help="Skip live HTTP requests")
    p_audit.set_defaults(func=cmd_audit)

    p_run = sub.add_parser("run-visibility", help="Execute multi-market Search & AI visibility run")
    p_run.add_argument("--mode", choices=["test", "live"], default="test", help="Run mode: test (no paid keys) or live")
    p_run.add_argument("--markets", default="US,IN,GB", help="Comma-separated markets (US,IN,GB)")
    p_run.add_argument("--providers", default="google_search,chatgpt,gemini,perplexity,claude", help="Comma-separated providers")
    p_run.add_argument("--limit", type=int, default=15, help="Max questions to process in this run")
    p_run.add_argument("--date", default=None, help="Observation date YYYY-MM-DD")
    p_run.add_argument("--pass-number", type=int, default=1, help="Verification pass number (1 or 2)")
    p_run.set_defaults(func=cmd_run_visibility)

    p_brief = sub.add_parser("generate-brief", help="Generate an AEO/GEO content brief for a question")
    p_brief.add_argument("--question-id", default="Q-001", help="Target Question ID (e.g. Q-001)")
    p_brief.add_argument("--content-type", default="how_to_guide", help="Content type")
    p_brief.set_defaults(func=cmd_generate_brief)

    p_rep = sub.add_parser("generate-report", help="Generate weekly visibility report")
    p_rep.set_defaults(func=cmd_generate_report)

    p_exp = sub.add_parser("export-all", help="Export all CSVs and assessment workbook bundle")
    p_exp.set_defaults(func=cmd_export_all)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
