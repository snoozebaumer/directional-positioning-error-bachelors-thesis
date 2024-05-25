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
df['wettereinschaetzung_regnerisch'] = (df['wettereinschaetzung'] == 'regnerisch').astype(int)
df['wettereinschaetzung_bewoelkt'] = (df['wettereinschaetzung'] == 'bewoelkt').astype(int)
df['wettereinschaetzung_sonnig'] = (df['wettereinschaetzung'] == 'sonnig').astype(int)
df['personenvorkommnis_viel'] = (df['personenvorkommnis'] == 'viel').astype(int)
df['personenvorkommnis_mittelmaessig'] = (df['personenvorkommnis'] == 'mittelmaessig').astype(int)
df['personenvorkommnis_wenig'] = (df['personenvorkommnis'] == 'wenig').astype(int)

# Add these new boolean columns to the list of boolean columns
boolean_columns.extend(['measureLocation_Bundesplatz', 'measureLocation_Fussgaenger', 'measureLocation_Zugersee',
                        'stage_Everything enabled', 'stage_No WiFi-Scanning','stage_No WiFi & BT-Scanning',
                        'stage_No BT-Scanning', 'stage_GPS Only', 'wettereinschaetzung_regnerisch',
                        'wettereinschaetzung_bewoelkt', 'wettereinschaetzung_sonnig', 'personenvorkommnis_viel',
                        'personenvorkommnis_mittelmaessig', 'personenvorkommnis_wenig'])

# Calculate the point-biserial correlation coefficient for each boolean column manually
correlation_results = {}

target_columns = ['latDifference', 'lonDifference', 'distance']
for target_col in target_columns:
    correlation_results[target_col + '_corr'] = []
    correlation_results[target_col + '_pval'] = []

for col in boolean_columns:
    for target_col in target_columns:
        if df[target_col].dtype in ['int64', 'float64']:
            # Filter out NaNs and infs
            valid_data = df[[col, target_col]].replace([np.inf, -np.inf], np.nan).dropna()
            if len(valid_data) > 0:
                correlation, p_value = stats.pointbiserialr(valid_data[col], valid_data[target_col])
                correlation_results[target_col + '_corr'].append(correlation)
                correlation_results[target_col + '_pval'].append(p_value)
            else:
                correlation_results[target_col + '_corr'].append(np.nan)
                correlation_results[target_col + '_pval'].append(np.nan)

# Create a DataFrame with the correlation results
correlation_df = pd.DataFrame(correlation_results, index=boolean_columns)

# Save the DataFrame to a CSV file
correlation_df.to_csv('correlations_boolean_categorical.csv', index=True)


# Display the correlation DataFrame
print(correlation_df)