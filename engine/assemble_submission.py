import shutil
from pathlib import Path
from engine.db import ROOT_DIR, EXPORTS_DIR, EVIDENCE_DIR
from engine.workbook_exporter import populate_and_save_submission_workbook, generate_official_visibility_csv

def assemble_submission():
    sub_dir = ROOT_DIR / "submission"
    sub_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. submission/workbook/
    wb_dir = sub_dir / "workbook"
    wb_dir.mkdir(parents=True, exist_ok=True)
    populate_and_save_submission_workbook(wb_dir / "IncuBrix_2027_Growth_Engineer_Option_3_AEO_SEO_GEO_Submission_Workbook.xlsx")
    for f in (EXPORTS_DIR / "workbook").glob("*.csv"):
        shutil.copy(f, wb_dir / f.name)
    if (EXPORTS_DIR / "workbook" / "assessment_workbook_bundle.json").exists():
        shutil.copy(EXPORTS_DIR / "workbook" / "assessment_workbook_bundle.json", wb_dir / "assessment_workbook_bundle.json")
    print("1. Assembled submission/workbook/")

    # 2. submission/visibility/
    vis_dir = sub_dir / "visibility"
    vis_dir.mkdir(parents=True, exist_ok=True)
    generate_official_visibility_csv(vis_dir / "visibility.csv")
    if (EXPORTS_DIR / "visibility_observations.csv").exists():
        shutil.copy(EXPORTS_DIR / "visibility_observations.csv", vis_dir / "visibility_observations.csv")
    print("2. Assembled submission/visibility/")

    # 3. submission/evidence/
    ev_dir = sub_dir / "evidence"
    ev_dir.mkdir(parents=True, exist_ok=True)
    for sub in ["crawl", "observations", "citations"]:
        src_sub = EVIDENCE_DIR / sub
        dst_sub = ev_dir / sub
        if src_sub.exists():
            if dst_sub.exists():
                shutil.rmtree(dst_sub)
            shutil.copytree(src_sub, dst_sub)
    if (EVIDENCE_DIR / "live_gemini_verified.json").exists():
        shutil.copy(EVIDENCE_DIR / "live_gemini_verified.json", ev_dir / "live_gemini_verified.json")
    print("3. Assembled submission/evidence/")

    # 4. submission/technical_fixes/
    tf_dir = sub_dir / "technical_fixes"
    tf_dir.mkdir(parents=True, exist_ok=True)
    if (ROOT_DIR / "TECHNICAL_SEO_AUDIT.md").exists():
        shutil.copy(ROOT_DIR / "TECHNICAL_SEO_AUDIT.md", tf_dir / "TECHNICAL_SEO_AUDIT.md")
    patches_dst = tf_dir / "patches"
    patches_src = ROOT_DIR / "data" / "patches"
    if patches_src.exists():
        if patches_dst.exists():
            shutil.rmtree(patches_dst)
        shutil.copytree(patches_src, patches_dst)
    print("4. Assembled submission/technical_fixes/")

    # 5. submission/content_pages/
    cp_dir = sub_dir / "content_pages"
    cp_dir.mkdir(parents=True, exist_ok=True)
    if (ROOT_DIR / "CONTENT_QUALITY_REPORT.md").exists():
        shutil.copy(ROOT_DIR / "CONTENT_QUALITY_REPORT.md", cp_dir / "CONTENT_QUALITY_REPORT.md")
    for f in (EXPORTS_DIR / "content_pages").glob("*.*"):
        shutil.copy(f, cp_dir / f.name)
    print("5. Assembled submission/content_pages/")

    # 6. submission/citation_plan/
    cit_dir = sub_dir / "citation_plan"
    cit_dir.mkdir(parents=True, exist_ok=True)
    if (ROOT_DIR / "CITATION_OPPORTUNITY_REPORT.md").exists():
        shutil.copy(ROOT_DIR / "CITATION_OPPORTUNITY_REPORT.md", cit_dir / "CITATION_OPPORTUNITY_REPORT.md")
    if (EXPORTS_DIR / "citation_opportunities_30.csv").exists():
        shutil.copy(EXPORTS_DIR / "citation_opportunities_30.csv", cit_dir / "citation_opportunities_30.csv")
    print("6. Assembled submission/citation_plan/")

    # 7. submission/reports/
    rep_dir = sub_dir / "reports"
    rep_dir.mkdir(parents=True, exist_ok=True)
    for doc in ["PROJECT_AUDIT.md", "PRODUCT_MARKET_INSIGHTS.md", "FINAL_TEST_REPORT.md", "SUBMISSION_CHECKLIST.md", "FINAL_INDEPENDENT_AUDIT.md", "REMAINING_LIMITATIONS.md"]:
        if (ROOT_DIR / doc).exists():
            shutil.copy(ROOT_DIR / doc, rep_dir / doc)
    if (EXPORTS_DIR / "weekly_visibility_report.md").exists():
        shutil.copy(EXPORTS_DIR / "weekly_visibility_report.md", rep_dir / "weekly_visibility_report.md")
    print("7. Assembled submission/reports/")

    # 8. submission/launch_kit/
    lk_dir = sub_dir / "launch_kit"
    lk_dir.mkdir(parents=True, exist_ok=True)
    if (EXPORTS_DIR / "workbook" / "06_launch_plan_90_days.csv").exists():
        shutil.copy(EXPORTS_DIR / "workbook" / "06_launch_plan_90_days.csv", lk_dir / "06_launch_plan_90_days.csv")
    print("8. Assembled submission/launch_kit/")

    # 9. submission/videos/
    vid_dir = sub_dir / "videos"
    vid_dir.mkdir(parents=True, exist_ok=True)
    print("9. Assembled submission/videos/")

if __name__ == "__main__":
    assemble_submission()

