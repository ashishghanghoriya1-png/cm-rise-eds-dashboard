import sys, io, os
import pymupdf

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

print("=== READING ALL KEY REPORT FINDINGS ===")

# Read Empirical_CPD_EDS_Research_Report.md
md_path = "C:/Users/Peepul/.gemini/antigravity/brain/d4007b68-e6ed-4169-8e19-8fc047825bef/Empirical_CPD_EDS_Research_Report.md"
if os.path.exists(md_path):
    print("\n--- Empirical_CPD_EDS_Research_Report.md ---")
    with open(md_path, "r", encoding="utf-8") as f:
        print(f.read()[:2000])

# Inspect PDF Reports
for pdf in ["PowerBI_Dashboard_Comprehensive_Report.pdf", "TabFM_PowerBI_Integrated_Predictions.pdf", "Observation_Field_Insights.pdf"]:
    full_p = os.path.join("c:/My Files Work/Gravity", pdf)
    if os.path.exists(full_p):
        print(f"\n--- PDF: {pdf} ---")
        doc = pymupdf.open(full_p)
        for i, page in enumerate(doc):
            if i < 2:
                print(f"Page {i+1}:", page.get_text()[:400].replace("\n", " "))

# Inspect discover_novel_deep_insights.py if exists
script_p = "c:/My Files Work/Gravity/discover_novel_deep_insights.py"
if os.path.exists(script_p):
    print("\n--- discover_novel_deep_insights.py ---")
    with open(script_p, "r", encoding="utf-8") as f:
        print(f.read()[:1500])
