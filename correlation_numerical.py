import pandas as pd
from IPython.display import display

FILE_PATH = "data/messungen_ueber_7m.txt"
df = pd.read_csv(FILE_PATH, delimiter='\t', encoding="iso-8859-1")

# Selecting the relevant columns
relevant_columns = ['latDifference', 'lonDifference', 'distance']

df.replace('WAHR', 1, inplace=True)
df.replace('FALSCH', 0, inplace=True)

# Converting all columns to numeric where possible
dataframe = df.apply(pd.to_numeric, errors='coerce')

# Fill missing values with mean
dataframe.fillna(dataframe.mean(), inplace=True)

# Calculating the correlation of all columns with the relevant columns
correlation_with_relevant = dataframe.corr()[relevant_columns]

# Extracting correlations of all attributes with latDifference, lonDifference, and distance
correlations = correlation_with_relevant.loc[:, relevant_columns]

# csv export
# correlations.to_csv('correlations.csv', index=True)

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
display(correlations, raw=True)
correlations
