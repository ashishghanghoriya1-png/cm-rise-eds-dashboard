import pandas as pd
import numpy as np
import sys

sys.stdout.reconfigure(encoding='utf-8')

july_path = 'EDS_Cleaned_Master_2July.xlsx'
aug_path = 'EDS_Full Data Table Consolidation_30 Aug.xlsx'

xls_july = pd.ExcelFile(july_path)
xls_aug = pd.ExcelFile(aug_path)

df_quant = pd.read_excel(xls_july, 'Quant_Structured').iloc[1:61].reset_index(drop=True)
df_qual = pd.read_excel(xls_july, 'Qual_FreeText').iloc[1:61].reset_index(drop=True)
df_obs = pd.read_excel(xls_july, 'Obs_Observations').iloc[1:61].reset_index(drop=True)
df_sheet1 = pd.read_excel(xls_july, 'Sheet1')
df_sheet2 = pd.read_excel(xls_july, 'Sheet2')

print("=" * 100)
print("DEEP AUDIT OF INACCURACIES, CONTRADICTIONS AND DATA FLAWS IN EDS_Cleaned_Master_2July.xlsx")
print("=" * 100)

inaccuracies = []

# -----------------------------------------------------------------------------
# 1. Contradictions between Participation Flag and Detailed Counts
# -----------------------------------------------------------------------------
# 1.1 CLSS Participation Flag vs No of CLSS Attended
# Col 18: 'Activities participated over 2025-26 academic year__CLSS'
# Col 68: 'No. of CLSS attended by teacher'
for idx, row in df_quant.iterrows():
    tid = row['Teacher_ID']
    flag = row['Activities participated over 2025-26 academic year__CLSS']
    att_no = row['No. of CLSS attended by teacher']
    
    # If flag == 0 but att_no > 0
    if flag == 0 and pd.notna(att_no) and str(att_no).strip() not in ['0', 'Not Participated', 'nan']:
        inaccuracies.append({
            'Category': 'CLSS Participation Contradiction',
            'Teacher_ID': tid,
            'Field 1': f"CLSS Flag (Col 18) = {flag}",
            'Field 2': f"No. of CLSS Attended (Col 68) = {att_no}",
            'Explanation': f"Teacher {tid} is marked as NOT participating in CLSS in Col 18, but Col 68 states they attended {att_no} CLSS sessions!"
        })
    elif flag == 1 and str(att_no).strip() in ['Not Participated']:
        inaccuracies.append({
            'Category': 'CLSS Participation Contradiction',
            'Teacher_ID': tid,
            'Field 1': f"CLSS Flag (Col 18) = {flag}",
            'Field 2': f"No. of CLSS Attended (Col 68) = {att_no}",
            'Explanation': f"Teacher {tid} is marked as participating in CLSS in Col 18, but Col 68 states 'Not Participated'!"
        })

# 1.2 Subject Training Participation Flag vs Training Useful rating
# Col 16: 'Activities participated over 2025-26 academic year__Subject Training'
# Col 28: 'Do teachers find subject in-person training useful or helpful'
for idx, row in df_quant.iterrows():
    tid = row['Teacher_ID']
    flag = row['Activities participated over 2025-26 academic year__Subject Training']
    useful = row['Do teachers find subject in-person training useful or helpful']
    
    if flag == 0 and pd.notna(useful) and str(useful).strip() == 'Yes':
        inaccuracies.append({
            'Category': 'Subject Training Contradiction',
            'Teacher_ID': tid,
            'Field 1': f"Subject Training Flag (Col 16) = {flag}",
            'Field 2': f"Training Useful (Col 28) = {useful}",
            'Explanation': f"Teacher {tid} is marked as NOT participating in Subject Training in Col 16, but Col 28 states they found Subject Training useful!"
        })

# 1.3 Online Course Completed Flag vs Platform Used / Diksha Course
# Col 37: 'Are there any online courses teacher has done in last 1 year'
# Col 96: 'Name of the online platforms used by the teacher'
# Col 102: 'Did Online Course'
for idx, row in df_quant.iterrows():
    tid = row['Teacher_ID']
    col37 = str(row['Are there any online courses teacher has done in last 1 year']).strip()
    col96 = str(row['Name of the online platforms used by the teacher']).strip()
    col102 = str(row['Did Online Course']).strip()
    
    if col37 == 'No' and col96 not in ['nan', '', 'None', 'No']:
        inaccuracies.append({
            'Category': 'Online Course Contradiction',
            'Teacher_ID': tid,
            'Field 1': f"Done Online Course (Col 37) = {col37}",
            'Field 2': f"Platforms Used (Col 96) = {col96}",
            'Explanation': f"Teacher {tid} claims NO online course done in last 1 year (Col 37), but Col 96 lists platforms used: '{col96}'!"
        })
    if col37 == 'Yes' and col102 in ['0', 'No', 'False']:
        inaccuracies.append({
            'Category': 'Online Course Flag Contradiction',
            'Teacher_ID': tid,
            'Field 1': f"Col 37 = {col37}",
            'Field 2': f"Col 102 (Did Online Course) = {col102}",
            'Explanation': f"Teacher {tid} has Col 37 = Yes, but derivative Col 102 = {col102}!"
        })

# 1.4 Topic Recall vs Topic Recalled Checkboxes
# Col 74: 'CLSS topics recalled__No topic recalled'
# Cols 69-73: Named topics recalled
topic_cols = [
    'CLSS topics recalled__कक्षा प्रबंधन के शुरुआती प्रयास',
    'CLSS topics recalled__पूर्वज्ञान से शुरु, समूहकार्य से सीख',
    'CLSS topics recalled__प्रभावी गृहकार्य',
    'CLSS topics recalled__पुनरवलोकन एवं समेकन',
    'CLSS topics recalled__प्रभावी पुनरावृत्ति'
]
for idx, row in df_quant.iterrows():
    tid = row['Teacher_ID']
    no_recall_flag = row['CLSS topics recalled__No topic recalled']
    recalled_any = any(row[c] == 1 for c in topic_cols if c in row)
    
    if no_recall_flag == 1 and recalled_any:
        inaccuracies.append({
            'Category': 'Topic Recall Contradiction',
            'Teacher_ID': tid,
            'Field 1': f"No Topic Recalled Flag = 1",
            'Field 2': f"Specific Topic Checked = True",
            'Explanation': f"Teacher {tid} is marked as 'No topic recalled' (Col 74 = 1) AND also has specific topic checkboxes checked!"
        })

# -----------------------------------------------------------------------------
# 2. Print Summary of Contradictions Found
# -----------------------------------------------------------------------------
print(f"\nTOTAL CONTRADICTIONS IDENTIFIED IN MASTER FILE: {len(inaccuracies)}")
for i, item in enumerate(inaccuracies, 1):
    print(f"\n[{i}] Category: {item['Category']}")
    print(f"    Teacher_ID: {item['Teacher_ID']}")
    print(f"    {item['Field 1']}  vs  {item['Field 2']}")
    print(f"    Explanation: {item['Explanation']}")

# -----------------------------------------------------------------------------
# 3. Check Demographic Data Mismatches between Quant, Qual, and Obs
# -----------------------------------------------------------------------------
print("\n" + "="*100)
print("DEMOGRAPHIC & METADATA MISMATCHES BETWEEN QUANT, QUAL AND OBS SHEETS")
print("="*100)

demo_cols = [
    'Name of the interviewer', 'Name of the note-taker', 
    'District of respondent teacher', 'Gender of respondent', 
    'Date of the interview', 'Subject taught by teacher', 
    'Years of teaching experience'
]

mismatches = []
for idx in range(60):
    tid = df_quant.iloc[idx]['Teacher_ID']
    for col in demo_cols:
        val_q = str(df_quant.iloc[idx][col]).strip() if col in df_quant.columns and pd.notna(df_quant.iloc[idx][col]) else "NaN"
        val_ql = str(df_qual.iloc[idx][col]).strip() if col in df_qual.columns and pd.notna(df_qual.iloc[idx][col]) else "NaN"
        val_o = str(df_obs.iloc[idx][col]).strip() if col in df_obs.columns and pd.notna(df_obs.iloc[idx][col]) else "NaN"
        
        # Standardize date strings if needed
        if 'Date' in col:
            val_q = val_q.split(' ')[0]
            val_ql = val_ql.split(' ')[0]
            val_o = val_o.split(' ')[0]
            
        if not (val_q == val_ql == val_o):
            mismatches.append({
                'Teacher_ID': tid,
                'Column': col,
                'Quant': val_q,
                'Qual': val_ql,
                'Obs': val_o
            })

print(f"TOTAL DEMOGRAPHIC MISMATCHES FOUND BETWEEN SHEETS: {len(mismatches)}")
for m in mismatches[:20]:
    print(f"  Teacher {m['Teacher_ID']} | Col: '{m['Column']}' -> Quant: '{m['Quant']}' | Qual: '{m['Qual']}' | Obs: '{m['Obs']}'")
if len(mismatches) > 20:
    print(f"  ... and {len(mismatches)-20} more demographic mismatches!")

