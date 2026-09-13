import pandas as pd
import numpy as np
import sys

sys.stdout.reconfigure(encoding='utf-8')

aug_path = 'EDS_Full Data Table Consolidation_30 Aug.xlsx'
july_path = 'EDS_Cleaned_Master_2July.xlsx'

xls_aug = pd.ExcelFile(aug_path)
xls_july = pd.ExcelFile(july_path)

df_quant = pd.read_excel(xls_july, 'Quant_Structured').iloc[1:61].reset_index(drop=True)
df_qual = pd.read_excel(xls_july, 'Qual_FreeText').iloc[1:61].reset_index(drop=True)
df_obs = pd.read_excel(xls_july, 'Obs_Observations').iloc[1:61].reset_index(drop=True)
df_sheet2 = pd.read_excel(xls_july, 'Sheet2').iloc[1:61].reset_index(drop=True)

print("=" * 80)
print("COMPREHENSIVE DISCREPANCY AUDIT: 30 AUG CONSOLIDATION VS 2 JULY CLEANED MASTER")
print("=" * 80)

# Helper function to print audit sections
def audit_header(title):
    print(f"\n{'='*80}\n{title}\n{'='*80}")

# ---------------------------------------------------------
# SHEET 1: Digital Course Data
# ---------------------------------------------------------
audit_header("1. AUDIT: Digital Course Data Sheet")

# 1.1 Completion rate / participation
# 30 Aug says: 52 out of 60 teachers (87%) completed online courses in last 1 year.
done_online = df_quant['Are there any online courses teacher has done in last 1 year'].value_counts()
print(f"[CHECK 1.1] Online course completed (Quant Col 37):")
print(done_online)
yes_cnt = done_online.get('Yes', 0)
no_cnt = done_online.get('No', 0)
pct_yes = (yes_cnt / 60) * 100
print(f"-> 2July Data: Yes={yes_cnt}/60 ({pct_yes:.1f}%), No={no_cnt}/60 ({(no_cnt/60)*100:.1f}%)")

# 1.2 Awareness of DIKSHA
# Quant Col 62: 'Does teacher know about DIKSHA Courses and platform'
diksha_know = df_quant['Does teacher know about DIKSHA Courses and platform'].value_counts(dropna=False)
print(f"\n[CHECK 1.2] Awareness of DIKSHA (Quant Col 62):")
print(diksha_know)
print("-> Note: 37 NaN, 23 Yes. Out of 60, only 23 explicitly marked Yes, 37 missing.")

# 1.3 Digital courses effective way to learn
# Quant Col 38: 'Does teacher think digital or online courses are an effective way for teachers to learn'
eff_cnts = df_quant['Does teacher think digital or online courses are an effective way for teachers to learn'].value_counts(dropna=False)
print(f"\n[CHECK 1.3] Effectiveness perception (Quant Col 38):")
print(eff_cnts)

# 1.4 Hours allocated to digital learning
hrs_cnts = df_quant['How many hours teacher can allocate to engage with digital courses__ digital learning'].value_counts(dropna=False)
print(f"\n[CHECK 1.4] Hours allocated (Quant Col 39):")
print(hrs_cnts)

# 1.5 Preferred timing
t_school = df_quant['Timing to do online or digital courses__learning__During school hours'].value_counts().get(1, 0)
t_after = df_quant['Timing to do online or digital courses__learning__After school'].value_counts().get(1, 0)
t_holiday = df_quant['Timing to do online or digital courses__learning__During holidays or weekends'].value_counts().get(1, 0)
print(f"\n[CHECK 1.5] Preferred timing (N=60):")
print(f"  During school hours: {t_school}/60 ({(t_school/60)*100:.1f}%)")
print(f"  After school: {t_after}/60 ({(t_after/60)*100:.1f}%)")
print(f"  During holidays/weekends: {t_holiday}/60 ({(t_holiday/60)*100:.1f}%)")


# ---------------------------------------------------------
# SHEET 2: IPT Data (In-Person Training)
# ---------------------------------------------------------
audit_header("2. AUDIT: IPT Data Sheet")

# IPT participation (Quant Col 16: Subject Training)
ipt_part = df_quant['Activities participated over 2025-26 academic year__Subject Training'].value_counts(dropna=False)
print(f"[CHECK 2.1] Subject Training Participation (Quant Col 16):")
print(ipt_part)

ipt_useful = df_quant['Do teachers find subject in-person training useful or helpful'].value_counts(dropna=False)
print(f"\n[CHECK 2.2] In-Person Training Useful/Helpful (Quant Col 28):")
print(ipt_useful)

ipt_applied = df_quant['Have they applied given resources_teaching lesson plan__ modules in their classroom'].value_counts(dropna=False)
print(f"\n[CHECK 2.3] Applied given resources in classroom (Quant Col 33):")
print(ipt_applied)

# Training resources received
res_ppt = df_quant['Training resources received from in-person training__PPT'].value_counts().get(1, 0)
res_mod = df_quant['Training resources received from in-person training__Margdarshika_Teaching Plan__Modules'].value_counts().get(1, 0)
res_tot = df_quant['Training resources received from in-person training__ToT'].value_counts().get(1, 0)
res_not = df_quant['Training resources received from in-person training__Not received'].value_counts().get(1, 0)
print(f"\n[CHECK 2.4] Training resources received:")
print(f"  PPT: {res_ppt}")
print(f"  Margdarshika/Modules: {res_mod}")
print(f"  ToT: {res_tot}")
print(f"  Not received: {res_not}")


# ---------------------------------------------------------
# SHEET 3: CLSS Data (Shaikshik Samvaad)
# ---------------------------------------------------------
audit_header("3. AUDIT: CLSS Data Sheet")

clss_part = df_quant['Activities participated over 2025-26 academic year__CLSS'].value_counts(dropna=False)
print(f"[CHECK 3.1] CLSS Participation (Quant Col 18):")
print(clss_part)

clss_att_no = df_quant['No. of CLSS attended by teacher'].value_counts(dropna=False)
print(f"\n[CHECK 3.2] Number of CLSS attended (Quant Col 68):")
print(clss_att_no)

clss_solved = df_quant['CLSS learning solved classroom challenge'].value_counts(dropna=False)
print(f"\n[CHECK 3.3] CLSS solved classroom challenge (Quant Col 75):")
print(clss_solved)

clss_know = df_quant["Does teacher know about CLSS and it's format"].value_counts(dropna=False)
print(f"\n[CHECK 3.4] Knowledge of CLSS format (Quant Col 87):")
print(clss_know)

# Topics recalled
top_cols = [c for c in df_quant.columns if 'CLSS topics recalled' in c]
print(f"\n[CHECK 3.5] CLSS topics recalled:")
for c in top_cols:
    v = df_quant[c].value_counts().to_dict()
    print(f"  {c}: {v}")

# Cascading processes
casc_cols = [c for c in df_quant.columns if 'Processes to cascade CLSS' in c]
print(f"\n[CHECK 3.6] Processes to cascade CLSS:")
for c in casc_cols:
    v = df_quant[c].value_counts().to_dict()
    print(f"  {c}: {v}")


# ---------------------------------------------------------
# SHEET 4: CRO Data (Classroom Observation & Mentoring)
# ---------------------------------------------------------
audit_header("4. AUDIT: CRO Data Sheet")
print("Checking Obs_Observations columns...")
for col in df_obs.columns:
    print(f"  Obs col: {col} | Non-null count: {df_obs[col].notna().sum()}")


# ---------------------------------------------------------
# SHEET 5: Cross-Cutting Data Sheet
# ---------------------------------------------------------
audit_header("5. AUDIT: Cross-Cutting Data Sheet")

# Check Motivation coding Teacher IDs mentioned in 30 Aug Consolidation:
# Intrinsic Strong (5): T18, T22, T24, T35, T56
# Intrinsic Moderate (9): T5, T6, T23, T25, T36, T37, T39, T45, T60
# Mixed Intrinsic + Compliance (4): T3, T7, T48, T59
# Mixed Moderate + Suppression (8): T1, T4, T8, T9, T11, T20, T32, T57
# Compliance Primary (4): T16, T27, T46, T51
# Low/Absent (1): T58
# Cannot infer (1): T49

tids_groups = {
    'Intrinsic Strong': ['18', '22', '24', '35', '56'],
    'Intrinsic Moderate': ['5', '6', '23', '25', '36', '37', '39', '45', '60'],
    'Mixed Intrinsic + Compliance': ['3', '7', '48', '59'],
    'Mixed Moderate + Suppression': ['1', '4', '8', '9', '11', '20', '32', '57'],
    'Compliance Primary': ['16', '27', '46', '51'],
    'Low/Absent': ['58'],
    'Cannot infer': ['49']
}

all_tids_in_groups = []
for k, v in tids_groups.items():
    all_tids_in_groups.extend(v)
    print(f"  {k} count: {len(v)} -> {v}")

print(f"\nTotal teachers in 7 tiers listed: {len(all_tids_in_groups)}")
print(f"Unique teachers listed: {len(set(all_tids_in_groups))}")
missing_tids_from_32 = set([str(i) for i in range(1, 61)]) - set(all_tids_in_groups)
print(f"Teachers NOT in the 32 blank list ({len(missing_tids_from_32)}):", sorted([int(x) for x in missing_tids_from_32]))

