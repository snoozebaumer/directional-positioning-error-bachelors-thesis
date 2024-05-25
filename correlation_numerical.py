import pandas as pd
import scipy.stats as stats

FILE_PATH = "updated_data_total.csv"  # Update with your actual file path
df = pd.read_csv(FILE_PATH, delimiter='\t', encoding="iso-8859-1")

# Selecting the relevant columns
relevant_columns = ['latDifference', 'lonDifference', 'distance']

# Converting all columns to numeric where possible
dataframe = df.apply(pd.to_numeric, errors='coerce')

# Fill missing values with mean
dataframe.fillna(dataframe.mean(), inplace=True)


# Function to calculate correlations and p-values
def calculate_pearson_correlation(data, target_cols):
    correlations = pd.DataFrame(index=data.columns, columns=target_cols)
    p_values = pd.DataFrame(index=data.columns, columns=target_cols)

    for target in target_cols:
        for column in data.columns:
            if column == target:
                continue
            valid_data = data[[column, target]].dropna()
            if len(valid_data) > 1:
                corr, p_val = stats.pearsonr(valid_data[column], valid_data[target])
                correlations.at[column, target] = corr
                p_values.at[column, target] = p_val

    return correlations, p_values


# Calculate correlations and p-values for relevant columns
correlations, p_values = calculate_pearson_correlation(dataframe, relevant_columns)

# Export correlations and p-values to a single CSV file
results = pd.concat([correlations.add_suffix('_corr'), p_values.add_suffix('_pval')], axis=1)
results.to_csv('correlations_and_pvalues.csv')

print("Correlations and p-values have been exported to 'correlations_and_pvalues.csv'.")