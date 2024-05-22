import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

df = pd.read_csv("updated_data_total.csv", sep="\t", encoding="iso-8859-1")
plt.figure(figsize=(12, 8))

threshold = 250

# Filter out extreme outliers from distance, latDifference, and lonDifference
filtered_df = df[(df['distance'].abs() <= threshold) &
                 (df['latDifference'].abs() <= threshold) &
                 (df['lonDifference'].abs() <= threshold)]

# Create a melted dataframe for easier boxplot plotting
melted_df = pd.melt(filtered_df[['distance', 'lonDifference', 'latDifference']])

# Plotting the boxplot
sns.boxplot(x='variable', y='value', data=melted_df)
plt.title('Distanz, Laengengraddifferenz, Breitengraddifferenz')
plt.xlabel('Variable')
plt.ylabel('Meter')
plt.show()