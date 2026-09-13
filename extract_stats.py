import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
import pandas as pd, numpy as np

df = pd.read_excel("quant_structured_tabfm_regression_all_cols.xlsx")
p = pd.to_numeric(df["Avg no. of classroom periods taken in a day"], errors="coerce")
exp = pd.to_numeric(df["Years of teaching experience"], errors="coerce")
clss = pd.to_numeric(df["No. of CLSS attended by teacher"], errors="coerce")

def col_label(c):
    return c.split("__")[-1] if "__" in c else c

print("=== ACTIVITIES PARTICIPATED ===")
for c in [x for x in df.columns if "Activities participated" in x]:
    v = pd.to_numeric(df[c], errors="coerce").sum()
    print(f"  {col_label(c)}: {int(v)}")

print("\n=== TRAINING RESOURCES ===")
for c in [x for x in df.columns if "Training resources" in x]:
    v = pd.to_numeric(df[c], errors="coerce").sum()
    print(f"  {col_label(c)}: {int(v)}")

print("\n=== DIKSHA ENGAGING FEATURES ===")
for c in [x for x in df.columns if "Most engaging features" in x]:
    v = pd.to_numeric(df[c], errors="coerce").sum()
    print(f"  {col_label(c)}: {int(v)}")

print("\n=== DIKSHA BARRIERS ===")
for c in [x for x in df.columns if "Reason for not doing DIKSHA" in x]:
    v = pd.to_numeric(df[c], errors="coerce").sum()
    print(f"  {col_label(c)}: {int(v)}")

print("\n=== CLSS TOPICS RECALLED ===")
for c in [x for x in df.columns if "CLSS topics recalled" in x]:
    v = pd.to_numeric(df[c], errors="coerce").sum()
    print(f"  {col_label(c)}: {int(v)}")

print("\n=== CLSS CASCADE PROCESSES ===")
for c in [x for x in df.columns if "Processes to cascade" in x]:
    v = pd.to_numeric(df[c], errors="coerce").sum()
    print(f"  {col_label(c)}: {int(v)}")

print("\n=== CLSS NON-PARTICIPATION REASONS ===")
for c in [x for x in df.columns if "Reasons of non-participation" in x]:
    v = pd.to_numeric(df[c], errors="coerce").sum()
    print(f"  {col_label(c)}: {int(v)}")

print("\n=== RSK MP CHALLENGES ===")
for c in [x for x in df.columns if "challenges do they face" in x]:
    v = pd.to_numeric(df[c], errors="coerce").sum()
    print(f"  {col_label(c)}: {int(v)}")

print("\n=== DIKSHA INFO SOURCES ===")
for c in [x for x in df.columns if "Source of information on DIKSHA" in x]:
    v = pd.to_numeric(df[c], errors="coerce").sum()
    print(f"  {col_label(c)}: {int(v)}")

print("\n=== TIMING PREFERENCES ===")
for c in [x for x in df.columns if "Timing to do online" in x]:
    v = pd.to_numeric(df[c], errors="coerce").sum()
    print(f"  {col_label(c)}: {int(v)}")

print("\n=== KEY CATEGORICAL DISTRIBUTIONS ===")
cats = [
    "Does teacher find SKG Sheekh ki Yatra useful",
    "Does teacher find YTL useful",
    "Does teacher think digital or online courses are an effective way for teachers to learn",
    "Could teacher recall RSK MP as attendance platform for CLSS",
    "Have they applied given resources_teaching lesson plan__ modules in their classroom",
    "Do teachers find subject in-person training useful or helpful",
    "Are there any online courses teacher has done in last 1 year",
    "Does teacher know about DIKSHA Courses and platform",
    "CLSS learning solved classroom challenge",
]
for c in cats:
    if c in df.columns:
        print(f"\n  {c}:")
        for k, v in df[c].value_counts().items():
            print(f"    {k}: {v} ({v/60*100:.1f}%)")

print("\n=== DIGITAL HOURS ===")
print(df["How many hours teacher can allocate to engage with digital courses__ digital learning"].value_counts().to_dict())
