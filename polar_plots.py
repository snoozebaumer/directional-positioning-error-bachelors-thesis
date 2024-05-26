# coding=iso-8859-1
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

FILE_PATH = "updated_data_total.csv"

df = pd.read_csv(FILE_PATH, encoding='latin1', sep='\t')

# Displaying the first few rows
df.head()


def create_polar_plot(data, title):
    # Calculate the angle and radius
    angles = np.arctan2(data['lonDifference'], data['latDifference'])
    radii = np.sqrt(data['latDifference'] ** 2 + data['lonDifference'] ** 2)

    # Convert angles to the range [0, 2*pi]
    angles = np.mod(angles, 2 * np.pi)

    # Create polar plot
    fig = plt.figure(figsize=(5, 5))
    ax = fig.add_subplot(111, polar=True)
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)

    # Plotting the data
    bars = ax.bar(angles, radii, width=0.1, color='grey', alpha=0.5)

    # Set title
    ax.set_title(title, va='bottom', fontsize=15)

    # Add cardinal directions
    ax.set_xticks(np.pi / 180. * np.linspace(0, 360, 8, endpoint=False))
    ax.set_xticklabels(['N', '', 'E', '', 'S', '', 'W', ''])

    plt.show()


# Create polar plots for each location
for location in ['Zugersee', 'Bundesplatz', 'Fussgänger']:
    location_data = df[df['measureLocation'] == location]
    create_polar_plot(location_data, f'{location}')

# Create polar plots for each stage
for stage in ['Everything enabled', 'No WiFi & BT-Scanning', 'No WiFi-Scanning', 'No BT-Scanning', 'GPS Only']:
    stage_data = df[df['stage'] == stage]
    create_polar_plot(stage_data, f'{stage}')
