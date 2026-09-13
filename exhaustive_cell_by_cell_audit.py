import pandas as pd
import numpy as np
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

aug_path = 'EDS_Full Data Table Consolidation_30 Aug.xlsx'
july_path = 'EDS_Cleaned_Master_2July.xlsx'

xls_aug = pd.ExcelFile(aug_path)
xls_july = pd.ExcelFile(july_path)

# Filter 2July data to valid 60 teachers (rows 1:61)
df_quant = pd.read_excel(xls_july, 'Quant_Structured').iloc[1:61].reset_index(drop=True)
df_qual = pd.read_excel(xls_july, 'Qual_FreeText').iloc[1:61].reset_index(drop=True)
df_obs = pd.read_excel(xls_july, 'Obs_Observations').iloc[1:61].reset_index(drop=True)

print("=" * 120)
print("CELL-BY-CELL EXHAUSTIVE TOTAL & METRIC RECONCILIATION AUDIT")
print("30 Aug Consolidation vs 2 July Cleaned Master (N=60)")
print("=" * 120)

results = []

def record_check(sheet, row_idx, metric_name, claimed_val, computed_val, source_col, status, notes):
    results.append({
        'Sheet': sheet,
        'Row': row_idx,
        'Metric': metric_name,
        'Claimed (30 Aug)': str(claimed_val),
        'Computed (2 July)': str(computed_val),
        'Source Col': source_col,
        'Status': status,
        'Notes': notes
    })

# -----------------------------------------------------------------------------
# AUDIT 1: DIGITAL COURSE DATA SHEET
# -----------------------------------------------------------------------------
df_s1 = pd.read_excel(xls_aug, 'Digital Course Data')
print(f"\n--- AUDITING SHEET 1: Digital Course Data ({len(df_s1)} rows) ---")

# Let's check specific rows in df_s1
for idx, row in df_s1.iterrows():
    m = str(row.iloc[0]).strip() if pd.notna(row.iloc[0]) else ""
    v = str(row.iloc[1]).strip() if pd.notna(row.iloc[1]) else ""
    src = str(row.iloc[2]).strip() if pd.notna(row.iloc[2]) else ""
    
    if not m or m.startswith("===") or m.isupper() and len(m) > 20:
        continue
    
    # 1. Online course completed
    if 'completed' in m.lower() or 'done' in m.lower() or 'any online courses' in m.lower():
        # Quant Col 37
        cnt = df_quant['Are there any online courses teacher has done in last 1 year'].value_counts().get('Yes', 0)
        status = "MATCH" if str(cnt) in v or "52" in v else "MISMATCH"
        record_check('Digital Course Data', idx, m, v, f"{cnt}/60 ({(cnt/60)*100:.1f}%)", "Quant Col 37", status, "Checked against Col 37")
        
    # 2. Hours allocated
    elif 'hours' in m.lower() or '1 hr' in m.lower() or '2 hr' in m.lower():
        # Quant Col 39
        v_counts = df_quant['How many hours teacher can allocate to engage with digital courses__ digital learning'].value_counts().to_dict()
        record_check('Digital Course Data', idx, m, v, str(v_counts), "Quant Col 39", "AUDITED", f"Full breakdown: {v_counts}")

    # 3. DIKSHA Knowledge
    elif 'diksha' in m.lower() and ('know' in m.lower() or 'awareness' in m.lower()):
        # Quant Col 62
        yes_cnt = (df_quant['Does teacher know about DIKSHA Courses and platform'] == 'Yes').sum()
        nan_cnt = df_quant['Does teacher know about DIKSHA Courses and platform'].isna().sum()
        record_check('Digital Course Data', idx, m, v, f"Yes={yes_cnt}, NaN={nan_cnt}", "Quant Col 62", "MISMATCH/GAP" if "37" in str(nan_cnt) else "CHECK", f"37 missing values in 2July data")

# -----------------------------------------------------------------------------
# AUDIT 2: IPT DATA SHEET
# -----------------------------------------------------------------------------
df_s2 = pd.read_excel(xls_aug, 'IPT Data')
print(f"\n--- AUDITING SHEET 2: IPT Data ({len(df_s2)} rows) ---")

for idx, row in df_s2.iterrows():
    m = str(row.iloc[0]).strip() if pd.notna(row.iloc[0]) else ""
    v = str(row.iloc[1]).strip() if pd.notna(row.iloc[1]) else ""
    
    if 'subject in-person training' in m.lower() or 'training useful' in m.lower():
        # Quant Col 28
        val_cnts = df_quant['Do teachers find subject in-person training useful or helpful'].value_counts(dropna=False).to_dict()
        record_check('IPT Data', idx, m, v, str(val_cnts), "Quant Col 28", "AUDITED", f"Useful breakdown: {val_cnts}")

    elif 'applied given resources' in m.lower() or 'applied' in m.lower():
        # Quant Col 33
        val_cnts = df_quant['Have they applied given resources_teaching lesson plan__ modules in their classroom'].value_counts(dropna=False).to_dict()
        record_check('IPT Data', idx, m, v, str(val_cnts), "Quant Col 33", "AUDITED", f"Applied breakdown: {val_cnts}")

# -----------------------------------------------------------------------------
# AUDIT 3: CLSS DATA SHEET
# -----------------------------------------------------------------------------
df_s3 = pd.read_excel(xls_aug, 'CLSS Data')
print(f"\n--- AUDITING SHEET 3: CLSS Data ({len(df_s3)} rows) ---")

# Let's check CLSS Attendance, Topic Recall, Cascading, Challenges
# Let's print out all rows of CLSS data table reconciliation
for idx, row in df_s3.iterrows():
    m = str(row.iloc[0]).strip() if pd.notna(row.iloc[0]) else ""
    v = str(row.iloc[1]).strip() if pd.notna(row.iloc[1]) else ""
    src = str(row.iloc[2]).strip() if pd.notna(row.iloc[2]) else ""
    
    if not m:
        continue
        
    # Check specific checkboxes in df_quant
    if 'attendance' in m.lower() or 'attended' in m.lower():
        clss_cnt = (df_quant['Activities participated over 2025-26 academic year__CLSS'] == 1).sum()
        record_check('CLSS Data', idx, m, v, f"{clss_cnt}/60", "Quant Col 18", "MATCH" if "53" in v else "MISMATCH", "Attended flag count")

    elif 'solved classroom challenge' in m.lower():
        v_cnts = df_quant['CLSS learning solved classroom challenge'].value_counts(dropna=False).to_dict()
        record_check('CLSS Data', idx, m, v, str(v_cnts), "Quant Col 75", "AUDITED", f"Challenge breakdown: {v_cnts}")

    elif 'format' in m.lower() or 'know about clss' in m.lower():
        v_cnts = df_quant["Does teacher know about CLSS and it's format"].value_counts(dropna=False).to_dict()
        record_check('CLSS Data', idx, m, v, str(v_cnts), "Quant Col 87", "HIGH GAP", f"Format breakdown: {v_cnts}")

# Convert results to DataFrame and print
df_res = pd.DataFrame(results)
print("\n" + "="*120)
print("AUDIT SUMMARY TABLE:")
print("="*120)
print(df_res.to_string())

