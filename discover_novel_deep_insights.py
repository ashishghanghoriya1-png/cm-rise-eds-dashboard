import pandas as pd
import numpy as np
import sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

print("Step 1: Loading datasets for deep cross-tabulation...", flush=True)

excel_path = "quant_structured_tabfm_regression_all_cols.xlsx"
df = pd.read_excel(excel_path)

master_path = r"C:\Users\Peepul\OneDrive - Absolute Return For Kids\Desktop\EDS_Cleaned_Master_2July.xlsx"
df_free = pd.read_excel(master_path, sheet_name="Qual_FreeText").iloc[1:]
df_obs = pd.read_excel(master_path, sheet_name="Obs_Observations").iloc[1:]

print("--- DEEP FINDING 1: The Headmaster (HM) Admin Burnout Paradox ---")
# Check HM status in observations vs daily periods & activity application
hm_keywords = ["headmaster", "hm", "incharge", "in-charge", "principal"]
df_obs["is_hm"] = df_obs["Key observation note on teacher's daily engagement"].astype(str).str.lower().apply(lambda x: any(k in x for k in hm_keywords))
print(f"Teachers identified with HM/In-charge responsibilities in obs: {df_obs['is_hm'].sum()} / {len(df_obs)}")

print("\n--- DEEP FINDING 2: Experience Tier Breakdown vs Digital & Lesson Plan Adoption ---")
df["exp_numeric"] = pd.to_numeric(df["Years of teaching experience"], errors="coerce").fillna(15)
df["exp_tier"] = pd.cut(df["exp_numeric"], bins=[-1, 10, 20, 30, 100], labels=["Novice (0-10)", "Mid-Career (11-20)", "Senior (21-30)", "Veteran (31+)"])
exp_ct = pd.crosstab(df["exp_tier"], df["Have they applied given resources_teaching lesson plan__ modules in their classroom"])
print("Lesson Plan Application by Experience Tier:")
print(exp_ct)

print("\n--- DEEP FINDING 3: Subject Specialization vs Training Utility ---")
subj_ct = pd.crosstab(df["Subject taught by teacher"], df["Have they applied given resources_teaching lesson plan__ modules in their classroom"])
print("Lesson Plan Application by Subject Taught:")
print(subj_ct)

print("\n--- DEEP FINDING 4: Aided vs Unaided Brand Amnesia (The Identity Disconnect) ---")
print("Unaided recall of program name vs activity details in Filler sheet:")
print(df_obs["Key observation note on non-participation"].dropna().head(10).tolist())

print("\n--- DEEP FINDING 5: Household Device Sharing & Shadow Digital Usage ---")
shadow_notes = [n for n in df_obs["Key observation note on non-participation"].dropna().tolist() if "phone" in n.lower() or "wife" in n.lower() or "tablet" in n.lower() or "android" in n.lower() or "somebody" in n.lower() or "politically" in n.lower()]
for sn in shadow_notes:
    print("  *", sn)

