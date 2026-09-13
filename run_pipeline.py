import sys
import io
import pandas as pd
import numpy as np
from tabfm import TabFMRegressor
from tabfm import tabfm_v1_0_0_pytorch as tabfm_v1_0_0

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# 1. Read Excel workbook
excel_path = r"C:\Users\Peepul\OneDrive - Absolute Return For Kids\Documents\EDS_Cleaned_Master_2July.xlsx"
df = pd.read_excel(excel_path, sheet_name="Quant_Structured")

# Strip row 0 (duplicate column headers)
df = df.iloc[1:].reset_index(drop=True)

# 2. Select target column
target_col = "Avg no. of classroom periods taken in a day"
df[target_col] = pd.to_numeric(df[target_col], errors="coerce")

# Convert non-numeric / datetime columns to clean string format to avoid pandas fillna dtype mismatch
for col in df.columns:
    if col != target_col:
        df[col] = df[col].astype(str)

# 3. Split train and test (missing target values to predict)
train_df = df[df[target_col].notna()].copy()
test_df = df[df[target_col].isna()].copy()

print(f"Train samples: {len(train_df)} | Missing target samples to predict: {len(test_df)}")

X_train = train_df.drop(columns=[target_col])
y_train = train_df[target_col].values
X_test = test_df.drop(columns=[target_col])

# 4. Load TabFM model & fit regressor
print("Loading TabFM regression model...", flush=True)
model = tabfm_v1_0_0.load(model_type="regression")

print("Fitting TabFMRegressor...", flush=True)
reg = TabFMRegressor(model=model, n_estimators=4, num_folds_for_cv=2, verbose=False)
reg.fit(X_train, y_train)

# 5. Predict missing values
print("Predicting missing values...", flush=True)
preds = reg.predict(X_test)
print("Predicted values:", preds, flush=True)

# 6. Fill missing values in df and save to Excel
df.loc[df[target_col].isna(), target_col] = preds
output_file = "tabfm_predictions.xlsx"
df.to_excel(output_file, index=False)
print(f"Successfully saved predictions to '{output_file}'!", flush=True)
