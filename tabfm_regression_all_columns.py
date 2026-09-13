import sys
import io
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from tabfm import TabFMRegressor
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

print(f"Loaded dataset: {len(df)} teachers x {len(df.columns)} columns", flush=True)

# -------------------------------------------------------
# Encode all features as numeric for TabFMRegressor
# -------------------------------------------------------
# Build a numeric encoding of the full dataframe
from sklearn.preprocessing import OrdinalEncoder

print("Step 2: Loading TabFM Regression model...", flush=True)
model_reg = tabfm_v1_0_0.load(model_type="regression")
reg_engine = TabFMRegressor(
    model=model_reg,
    max_num_features=20,   # subsampling to avoid token limits
    n_estimators=1,
    num_folds_for_cv=1,
    verbose=False
)

# Record original dtypes & unique values per column
col_info = {}
for col in df.columns:
    numeric_series = pd.to_numeric(df[col], errors="coerce")
    is_numeric = numeric_series.notna().sum() / max(df[col].notna().sum(), 1) > 0.7
    col_info[col] = {
        "is_numeric": is_numeric,
        "unique_vals": sorted([str(v) for v in df[col].dropna().unique()])
    }

# Encode entire dataframe as numeric for regression context
df_encoded = df.copy()
enc = OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)
for col in df_encoded.columns:
    if col_info[col]["is_numeric"]:
        df_encoded[col] = pd.to_numeric(df_encoded[col], errors="coerce")
    else:
        df_encoded[col] = enc.fit_transform(df_encoded[[col]].astype(str))

imputation_summary = []

print("Step 3: Applying TabFM Regressor on ALL columns...", flush=True)
for i, col in enumerate(df.columns):
    missing_count = int(df[col].isna().sum())
    if missing_count == 0:
        print(f"[{i+1}/{len(df.columns)}] SKIP (no missing): '{col}'", flush=True)
        continue

    valid_mask = df_encoded[col].notna()
    missing_mask = df_encoded[col].isna()
    n_train = int(valid_mask.sum())
    n_test = int(missing_mask.sum())

    # Not enough training data fallback
    if n_train < 3:
        fill_val = 0.0
        df_encoded.loc[missing_mask, col] = fill_val
        df.loc[missing_mask, col] = fill_val
        imputation_summary.append({"column": col, "method": "Fallback (low train)", "missing": n_test})
        print(f"[{i+1}/{len(df.columns)}] FALLBACK: '{col}' (n_train={n_train})", flush=True)
        continue

    try:
        X_train = df_encoded.loc[valid_mask].drop(columns=[col]).fillna(0)
        y_train = df_encoded.loc[valid_mask, col].values.astype(float)
        X_test  = df_encoded.loc[missing_mask].drop(columns=[col]).fillna(0)

        reg_engine.fit(X_train, y_train)
        preds = reg_engine.predict(X_test)

        # For originally categorical columns: round to nearest known category encoding
        df_encoded.loc[missing_mask, col] = preds

        # Map back to original values for non-numeric columns
        if not col_info[col]["is_numeric"]:
            unique_enc_vals = df_encoded.loc[valid_mask, col].round().astype(int).clip(0)
            enc_to_orig = {}
            valid_orig = df.loc[valid_mask, col].astype(str).values
            valid_enc  = df_encoded.loc[valid_mask, col].round().astype(int).clip(0).values
            for ov, ev in zip(valid_orig, valid_enc):
                enc_to_orig[ev] = ov

            mapped_preds = []
            for pred_enc in preds:
                ridx = int(round(pred_enc))
                if ridx in enc_to_orig:
                    mapped_preds.append(enc_to_orig[ridx])
                else:
                    # nearest key
                    nearest = min(enc_to_orig.keys(), key=lambda k: abs(k - ridx))
                    mapped_preds.append(enc_to_orig[nearest])
            df.loc[missing_mask, col] = mapped_preds
        else:
            df.loc[missing_mask, col] = preds

        imputation_summary.append({
            "column": col,
            "method": "TabFM Regressor",
            "missing": n_test,
            "n_train": n_train
        })
        print(f"[{i+1}/{len(df.columns)}] TABFM REGRESSOR OK ({n_test} imputed): '{col}'", flush=True)

    except Exception as e:
        # Fallback to median/mode
        if col_info[col]["is_numeric"]:
            fill_val = pd.to_numeric(df[col], errors="coerce").median()
        else:
            mode_vals = df[col].dropna().mode()
            fill_val = mode_vals[0] if len(mode_vals) > 0 else "N/A"
        df.loc[missing_mask, col] = fill_val
        df_encoded.loc[missing_mask, col] = 0.0
        imputation_summary.append({"column": col, "method": f"Error fallback: {str(e)[:60]}", "missing": n_test})
        print(f"[{i+1}/{len(df.columns)}] ERROR FALLBACK: '{col}' -> {e}", flush=True)

# Final check
remaining_nans = int(df.isna().sum().sum())
print(f"\nStep 4: Imputation complete. Remaining NaNs: {remaining_nans}", flush=True)

print("Step 5: Exporting fully imputed dataset...", flush=True)
out_excel = "quant_structured_tabfm_regression_all_cols.xlsx"
df.to_excel(out_excel, index=False)
print(f"Saved '{out_excel}' with shape {df.shape} ({len(df)} Teachers x {len(df.columns)} Columns)!", flush=True)

# Save imputation summary
summary_df = pd.DataFrame(imputation_summary)
summary_df.to_excel("tabfm_regression_imputation_summary.xlsx", index=False)
print(f"Saved imputation summary with {len(summary_df)} rows.", flush=True)
