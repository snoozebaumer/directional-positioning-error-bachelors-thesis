# coding=iso-8859-1
import pandas as pd
import numpy as np
import scipy.stats as stats

# Load the dataset
file_path = 'updated_data_total.csv'
df = pd.read_csv(file_path, sep='\t', encoding="iso-8859-1")

# Replace "WAHR" with True and "FALSCH" with False
df.replace({'WAHR': True, 'FALSCH': False}, inplace=True)

# Ensure the boolean columns are correctly typed
boolean_columns = ['wifiScanning', 'wifiEnabled', 'bluetoothEnabled', 'bluetoothScanning']
for col in boolean_columns:
    df[col] = df[col].astype(bool)

# Encode measureLocation and stages into boolean values
df['measureLocation_Bundesplatz'] = (df['measureLocation'] == 'Bundesplatz').astype(int)
df['measureLocation_Fussgaenger'] = (df['measureLocation'] == 'Fussgänger').astype(int)
df['measureLocation_Zugersee'] = (df['measureLocation'] == 'Zugersee').astype(int)
df['stage_Everything enabled'] = (df['stage'] == 'Everything enabled').astype(int)
df['stage_No WiFi-Scanning'] = (df['stage'] == 'No WiFi-Scanning').astype(int)
df['stage_No WiFi & BT-Scanning'] = (df['stage'] == 'No WiFi & BT-Scanning').astype(int)
df['stage_No BT-Scanning'] = (df['stage'] == 'No BT-Scanning').astype(int)
df['stage_GPS Only'] = (df['stage'] == 'GPS Only').astype(int)


# Add these new boolean columns to the list of boolean columns
boolean_columns.extend(['measureLocation_Bundesplatz', 'measureLocation_Fussgaenger', 'measureLocation_Zugersee',
                        'stage_Everything enabled', 'stage_No WiFi-Scanning','stage_No WiFi & BT-Scanning',
                        'stage_No BT-Scanning', 'stage_GPS Only'])

# Calculate the point-biserial correlation coefficient for each boolean column manually
correlation_results = []

for col in boolean_columns:
    col_results = {'Column': col}
    for target_col in df.columns:
        if target_col != col and target_col in ['latDifference', 'lonDifference', 'distance']:
            if df[target_col].dtype in ['int64', 'float64']:
                # Filter out NaNs and infs
                valid_data = df[[col, target_col]].replace([np.inf, -np.inf], np.nan).dropna()
                if len(valid_data) > 0:
                    correlation, p_value = stats.pointbiserialr(valid_data[col], valid_data[target_col])
                    col_results[target_col] = correlation
    correlation_results.append(col_results)

# Convert the results to a DataFrame for easier visualization
correlation_df = pd.DataFrame(correlation_results)
correlation_df.to_csv('correlations_boolean_categorical.csv', index=True)

# Display the correlation DataFrame
print(correlation_df)