import sys
import io
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from tabfm import TabFMClassifier, TabFMRegressor
from tabfm import tabfm_v1_0_0_pytorch as tabfm_v1_0_0

print("Step 1: Reading Excel workbook (Quant_Structured sheet)...", flush=True)
excel_path = r"C:\Users\Peepul\OneDrive - Absolute Return For Kids\Documents\EDS_Cleaned_Master_2July.xlsx"
df = pd.read_excel(excel_path, sheet_name="Quant_Structured")

# Ensure all 60 study teachers (IDs 1 through 60) are included
existing_ids = set(df["Teacher_ID"].dropna().astype(int).tolist())
for tid in range(1, 61):
    if tid not in existing_ids:
        row = {col: None for col in df.columns}
        row["Teacher_ID"] = tid
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)

df["Teacher_ID"] = pd.to_numeric(df["Teacher_ID"], errors="coerce").astype(int)
df = df.sort_values("Teacher_ID").reset_index(drop=True)

print(f"Loaded dataset containing all {len(df)} study teachers (IDs 1 to {len(df)})", flush=True)

# Prepare clean feature matrix for TabFM
X_all = df.copy()
for col in X_all.columns:
    X_all[col] = X_all[col].astype(str)

print("Step 2: Loading TabFM Classification & Regression models...", flush=True)
model_clf = tabfm_v1_0_0.load(model_type="classification")
model_reg = tabfm_v1_0_0.load(model_type="regression")

clf_engine = TabFMClassifier(model=model_clf, max_num_features=20, n_estimators=1, num_folds_for_cv=1, verbose=False)
reg_engine = TabFMRegressor(model=model_reg, max_num_features=20, n_estimators=1, num_folds_for_cv=1, verbose=False)

imputation_summary = []

print("Step 3: Imputing missing values across all 103 columns for all 60 teachers...", flush=True)
for i, col in enumerate(df.columns):
    missing_count = df[col].isna().sum()
    if missing_count == 0:
        continue
    
    valid_mask = df[col].notna()
    missing_mask = df[col].isna()
    n_train = int(valid_mask.sum())
    n_test = int(missing_mask.sum())
    
    if n_train < 2 or n_test == len(df):
        fill_val = 0 if pd.api.types.is_numeric_dtype(df[col]) else "Not Specified"
        df.loc[missing_mask, col] = fill_val
        X_all.loc[missing_mask, col] = str(fill_val)
        imputation_summary.append({
            "column": col,
            "type": "Fallback",
            "missing_count": n_test,
            "train_count": n_train
        })
        continue
    
    train_vals = df.loc[valid_mask, col]
    unique_vals = set(train_vals.unique())
    n_unique = len(unique_vals)
    
    str_vals = {str(v).strip() for v in unique_vals}
    is_onehot_indicator = ("__" in col or str_vals.issubset({"0", "1", "0.0", "1.0", "nan"})) and n_unique <= 2
    
    try:
        if is_onehot_indicator:
            fill_val = 0 if any(isinstance(v, (int, float, np.number)) for v in unique_vals) else "0"
            df.loc[missing_mask, col] = fill_val
            X_all.loc[missing_mask, col] = str(fill_val)
            imputation_summary.append({
                "column": col,
                "type": "One-Hot Indicator (Default 0)",
                "missing_count": n_test,
                "train_count": n_train
            })
            print(f"[{i+1}/{len(df.columns)}] Imputed ONE-HOT INDICATOR: '{col}'", flush=True)
        elif n_unique <= 1:
            fill_val = train_vals.iloc[0]
            df.loc[missing_mask, col] = fill_val
            X_all.loc[missing_mask, col] = str(fill_val)
            imputation_summary.append({
                "column": col,
                "type": "Constant",
                "missing_count": n_test,
                "train_count": n_train
            })
            print(f"[{i+1}/{len(df.columns)}] Imputed CONSTANT: '{col}'", flush=True)
        elif n_unique <= 10:
            y_train = train_vals.astype(str).values
            X_tr = X_all[valid_mask].drop(columns=[col]).fillna("Missing")
            X_te = X_all[missing_mask].drop(columns=[col]).fillna("Missing")
            
            clf_engine.fit(X_tr, y_train)
            preds = clf_engine.predict(X_te)
            
            numeric_y = pd.to_numeric(train_vals, errors="coerce")
            if numeric_y.notna().all():
                preds = pd.to_numeric(preds, errors="coerce")
                
            df.loc[missing_mask, col] = preds
            X_all.loc[missing_mask, col] = [str(p) for p in preds]
            imputation_summary.append({
                "column": col,
                "type": f"TabFM Classifier ({n_unique} classes)",
                "missing_count": n_test,
                "train_count": n_train
            })
            print(f"[{i+1}/{len(df.columns)}] Imputed TABFM CLASSIFIER ({n_unique} classes): '{col}'", flush=True)
        else:
            numeric_y = pd.to_numeric(train_vals, errors="coerce")
            if numeric_y.notna().sum() / n_train > 0.8:
                y_train = numeric_y.values
                X_tr = X_all[valid_mask].drop(columns=[col]).fillna("Missing")
                X_te = X_all[missing_mask].drop(columns=[col]).fillna("Missing")
                
                reg_engine.fit(X_tr, y_train)
                preds = reg_engine.predict(X_te)
                df.loc[missing_mask, col] = preds
                X_all.loc[missing_mask, col] = [str(p) for p in preds]
                imputation_summary.append({
                    "column": col,
                    "type": "TabFM Regressor (Continuous)",
                    "missing_count": n_test,
                    "train_count": n_train
                })
                print(f"[{i+1}/{len(df.columns)}] Imputed TABFM REGRESSOR: '{col}'", flush=True)
            else:
                most_common = train_vals.mode()[0] if not train_vals.empty else "N/A"
                df.loc[missing_mask, col] = most_common
                X_all.loc[missing_mask, col] = str(most_common)
                imputation_summary.append({
                    "column": col,
                    "type": f"Mode Fallback ({n_unique} high cardinality classes)",
                    "missing_count": n_test,
                    "train_count": n_train
                })
                print(f"[{i+1}/{len(df.columns)}] Imputed MODE ({n_unique} classes): '{col}'", flush=True)
    except Exception as e:
        print(f"Fallback for '{col}': {e}", flush=True)
        most_common = train_vals.mode()[0] if not train_vals.empty else "N/A"
        df.loc[missing_mask, col] = most_common
        X_all.loc[missing_mask, col] = str(most_common)
        imputation_summary.append({
            "column": col,
            "type": "Error Fallback (Mode)",
            "missing_count": n_test,
            "train_count": n_train
        })

print("Step 4: Exporting 60-teacher fully populated dataset...", flush=True)
out_excel = "quant_structured_all_imputed.xlsx"
df.to_excel(out_excel, index=False)
print(f"Successfully processed all columns and saved '{out_excel}' with shape {df.shape} (60 Teachers)!", flush=True)
