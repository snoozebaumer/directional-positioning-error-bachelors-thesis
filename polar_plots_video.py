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
    bars = ax.bar(angles, radii, width=0.1, color='black', edgecolor='black', alpha=0.5)

    # Set title
    ax.set_title(title, va='bottom', fontsize=15, color='white')

    # Add cardinal directions
    ax.set_xticks(np.pi / 180. * np.linspace(0, 360, 8, endpoint=False))
    ax.set_xticklabels(['N', '', 'E', '', 'S', '', 'W', ''], color='white')

    ax.grid(color='white')
    ax.set_yticklabels(ax.get_yticks(), color='white')

    # Change the background color
    ax.set_facecolor('#0cc0df')
    fig.patch.set_facecolor('#0cc0df')

    plt.show()




i = 1
# Create polar plots for each location
for location in ['Zugersee', 'Bundesplatz', 'Fussgänger']:
    location_data = df[df['measureLocation'] == location]
    create_polar_plot(location_data, f'Point {i}')
    i = i + 1

# Create polar plots for each stage
for stage in ['Everything enabled', 'No WiFi & BT-Scanning', 'No WiFi-Scanning', 'No BT-Scanning', 'GPS Only']:
    stage_data = df[df['stage'] == stage]
    create_polar_plot(stage_data, f'{stage}')

# Filter the data for "cellTowerRsrp1" with RF Condition higher than -90
filtered_data = df[(df['cellTowerRsrp1'] > -90)]

# Create polar plot for the filtered data
create_polar_plot(filtered_data, 'Signalstärke des ersten Mobilfunkturms > -90')

