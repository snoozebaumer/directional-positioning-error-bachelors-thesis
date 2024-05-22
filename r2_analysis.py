import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer
from sklearn.metrics import r2_score

FILE_PATH = "updated_data_total.csv"
df = pd.read_csv(FILE_PATH, encoding="iso-8859-1", delimiter='\t')

# Replace "WAHR" with 1 and "FALSCH" with 0
df = df.replace({"WAHR": 1, "FALSCH": 0})

# Filter out non-numeric columns
df_numeric = df.select_dtypes(include=[np.number])

# Ensure all columns are preserved by filling NaNs with a placeholder (e.g., 0) before imputation
df_numeric_filled = df_numeric.fillna(0)

# Impute missing values (mean strategy)
imputer = SimpleImputer(strategy='mean')
df_imputed = imputer.fit_transform(df_numeric_filled)
df_imputed = pd.DataFrame(df_imputed, columns=df_numeric.columns)

# Function to calculate R2 values
def calculate_r2(df, target):
    r2_values = {}
    for column in df.columns:
        if column != target:
            X = df[[column]].values
            y = df[target].values
            model = LinearRegression()
            model.fit(X, y)
            y_pred = model.predict(X)
            r2_values[column] = r2_score(y, y_pred)
    return r2_values

# Calculate R2 values for each target
targets = ["distance", "latDifference", "lonDifference"]
r2_results = {target: calculate_r2(df_imputed, target) for target in targets}

# Print R2 values table
for target, r2_values in r2_results.items():
    print(f"R2 values for target: {target}")
    print("--------------------------------------")
    print("| Feature           | R2 Score       |")
    print("--------------------------------------")
    for feature, r2_score in r2_values.items():
        print(f"| {feature:<18} | {r2_score:.4f}    |")
    print("--------------------------------------")
    print()
