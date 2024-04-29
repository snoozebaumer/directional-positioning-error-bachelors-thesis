import matplotlib.pyplot as plt


# Function to plot latitudinal and longitudinal differences
def plot_differences(data, title, footer, lat_diff_index, lon_diff_index, max_diff):
    lat_diffs = [float(row.strip().split('\t')[lat_diff_index]) for row in data]
    lon_diffs = [float(row.strip().split('\t')[lon_diff_index]) for row in data]

    # Create a figure and axis
    fig, ax = plt.subplots()

    ax.axhline(0, color='black', linestyle='-', linewidth=0.5)
    ax.axvline(0, color='black', linestyle='-', linewidth=0.5)

    # Plot the latitudinal and longitudinal differences
    ax.scatter(lon_diffs, lat_diffs, marker='+', color='black')

    ax.set_xlabel('Long Differenz (m)')
    ax.set_ylabel('Lat Differenz (m)')
    ax.set_title(title)

    ax.text(0, -max_diff * 0.9, footer, horizontalalignment='center')

    # Add footer
    ax.text(0, -200, footer, horizontalalignment='center')

    ax.set_xlim(-max_diff, max_diff)
    ax.set_ylim(-max_diff, max_diff)

    # Show the plot
    plt.show()


# Function to read data from file and plot differences for every 20 measurements
def plot_differences_for_measurements(file_path):
    max_diff_overall = 0

    with open(file_path, 'r') as file:
        lines = file.readlines()
        header = lines[0].strip().split('\t')
        lat_diff_index = header.index('latDifference')
        lon_diff_index = header.index('lonDifference')
        lines = lines[1:]  # Remove header

        # Group measurements into chunks of 20
        chunks = [lines[i:i + 20] for i in range(0, len(lines), 20)]

        # Calculate max_diff_overall so all plots have the same boundaries, so we're able to compare them
        for chunk in chunks:
            lat_diffs = [float(row.strip().split('\t')[lat_diff_index]) for row in chunk]
            lon_diffs = [float(row.strip().split('\t')[lon_diff_index]) for row in chunk]
            max_diff_chunk = max(max(lat_diffs), max(lon_diffs), abs(min(lat_diffs)), abs(min(lon_diffs)))
            if max_diff_chunk > max_diff_overall:
                max_diff_overall = max_diff_chunk

        # Iterate over each chunk and plot differences
        for i, chunk in enumerate(chunks):
            first_measurement = chunk[0].strip().split('\t')
            stage = first_measurement[1]
            measure_location = first_measurement[2]
            timestamp = first_measurement[0]

            plot_differences(chunk, f'Ort: {measure_location}, Einstellung: {stage}', f'Start d. Messung: {timestamp}', lat_diff_index, lon_diff_index, max_diff_overall)


# Example usage
plot_differences_for_measurements('updated_data.csv')