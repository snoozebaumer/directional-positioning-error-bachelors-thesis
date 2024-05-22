import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Sample data loading - Replace this with actual data loading
df = pd.read_csv("updated_data_total.csv", sep="\t", encoding="iso-8859-1")


# Function to calculate the mean overall delta
# Function to calculate the mean overall delta for 'distance'
def calculate_mean_delta(df, filterLocation = ""):
    results = []
    locations = []
    current_location = None
    measurements = []

    for index, row in df.iterrows():
        if filterLocation != "" and filterLocation not in row['measureLocation']:
            continue

        # either the location changed or max measurements for a location (100) is reached
        if current_location != row['measureLocation'] or len(measurements) >= 100:
            if measurements:
                measurements_df = pd.DataFrame(measurements)
                first_measurement = measurements_df.iloc[0]['distance']
                median_measurement = measurements_df['distance'].median()

                # Calculate the delta
                delta = abs(first_measurement - median_measurement)

                results.append(delta)
                locations.append(current_location)

            # Reset for new location or after 100 measurements
            current_location = row['measureLocation']
            measurements = []

        # Add current row to measurements
        measurements.append(row)

    # Handle the last batch
    if measurements:
        measurements_df = pd.DataFrame(measurements)
        first_measurement = measurements_df.iloc[0]['distance']
        median_measurement = measurements_df['distance'].median()

        # Calculate the delta
        delta = abs(first_measurement - median_measurement)

        results.append(delta)
        locations.append(current_location)

    #plot results
    plt.figure(figsize=(10, 6))
    plt.scatter(locations, results, marker='o')
    plt.xlabel('Messort')
    plt.ylabel('Delta (m)')
    plt.title('Delta zwischen erster Messung und Median der Messreihe')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Calculate the mean of all the deltas
    overall_mean_delta = np.mean(results)

    # Calculate the median of all the deltas
    #overall_median_delta = np.median(results)

    return overall_mean_delta


mean_overall_delta = calculate_mean_delta(df)
print(f'Mean Overall Delta: {mean_overall_delta}')

mean_overall_delta = calculate_mean_delta(df, "Zugersee")
print(f'Mean Zugersee Delta: {mean_overall_delta}')

mean_overall_delta = calculate_mean_delta(df, "Bundesplatz")
print(f'Mean Bundesplatz Delta: {mean_overall_delta}')

mean_overall_delta = calculate_mean_delta(df, "Fussg")
print(f'Mean Fussgaenger Delta: {mean_overall_delta}')