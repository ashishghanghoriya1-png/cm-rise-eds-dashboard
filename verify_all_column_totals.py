import pandas as pd
import numpy as np
import sys

sys.stdout.reconfigure(encoding='utf-8')

july_path = 'EDS_Cleaned_Master_2July.xlsx'
xls_july = pd.ExcelFile(july_path)

df_quant = pd.read_excel(xls_july, 'Quant_Structured').iloc[1:61].reset_index(drop=True)
df_qual = pd.read_excel(xls_july, 'Qual_FreeText').iloc[1:61].reset_index(drop=True)
df_obs = pd.read_excel(xls_july, 'Obs_Observations').iloc[1:61].reset_index(drop=True)

print("=" * 120)
print("EXHAUSTIVE COLUMN TOTAL & DENOMINATOR RECONCILIATION FOR EDS_Cleaned_Master_2July.xlsx")
print("=" * 120)

column_audits = []

def audit_col_group(group_name, cols, total_n=60):
    print(f"\n--- GROUP: {group_name} ---")
    sum_ones = 0
    non_null_respondents = set()
    
    for c in cols:
        if c in df_quant.columns:
            cnt_1 = (df_quant[c] == 1).sum()
            cnt_non_null = df_quant[c].notna().sum()
            sum_ones += cnt_1
            val_counts = df_quant[c].value_counts(dropna=False).to_dict()
            print(f"  Col '{c}': 1s={cnt_1}, non-null={cnt_non_null}, values={val_counts}")
        else:
            print(f"  Col '{c}': MISSING FROM QUANT SHEET")
            
    print(f"  => SUM OF ALL SELECTIONS IN GROUP: {sum_ones}")
    print(f"  => AVERAGE PER TEACHER (N={total_n}): {sum_ones / total_n:.2f}")

# 1. Subject Training Resources Received (Cols 29-32)
res_cols = [
    'Training resources received from in-person training__PPT',
    'Training resources received from in-person training__Margdarshika_Teaching Plan__Modules',
    'Training resources received from in-person training__ToT',
    'Training resources received from in-person training__Not received'
]
audit_col_group("IPT Resources Received", res_cols)

# 2. DIKSHA Engaging Features (Cols 43-49)
diksha_feat_cols = [c for c in df_quant.columns if 'Most engaging features of DIKSHA' in c]
audit_col_group("DIKSHA Engaging Features", diksha_feat_cols)

# 3. DIKSHA Sources of Info (Cols 50-56)
diksha_src_cols = [c for c in df_quant.columns if 'Source of information on DIKSHA' in c]
audit_col_group("DIKSHA Sources of Information", diksha_src_cols)

# 4. CLSS Topics Recalled (Cols 69-74)
clss_topic_cols = [c for c in df_quant.columns if 'CLSS topics recalled' in c]
audit_col_group("CLSS Topics Recalled", clss_topic_cols, total_n=53)

# 5. CLSS Cascading Processes (Cols 76-80)
clss_casc_cols = [c for c in df_quant.columns if 'Processes to cascade CLSS' in c]
audit_col_group("CLSS Cascading Processes", clss_casc_cols, total_n=53)

# 6. CLSS Attendance Form Challenges (Cols 82-86)
clss_chal_cols = [c for c in df_quant.columns if 'What challenges do they face in filling attendance' in c]
audit_col_group("CLSS Attendance Form Challenges", clss_chal_cols, total_n=53)

# 7. Reasons for Non-Participation in CLSS (Cols 88-93)
clss_nonpart_cols = [c for c in df_quant.columns if 'Reasons of non-participation in CLSS' in c]
audit_col_group("Reasons for Non-Participation in CLSS", clss_nonpart_cols, total_n=7)

