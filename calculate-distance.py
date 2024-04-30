import math

# input file: the exported measurement csv file directly from Measuralyze application. No changes needed.
FILE_PATH = "data/measurements_20240430_104703_d2_p1.csv"


def haversine(lat1, lon1, lat2, lon2):
    """
    uses Haversine formula to calculate distance between two points
    on the Earth's surface given their latitude and longitude,
    accounting for earth's curvature
    """
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    deltaLon = lon2 - lon1
    deltaLat = lat2 - lat1
    a = math.sin(deltaLat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(deltaLon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    """ 
    according to https://rechneronline.de/earth-radius/, the earth radius for an elevation of 
    425m above sea level and a latitude of 47 (most of Switzerland) is 6367.168 km, instead of the
    rounded 6371 that would be standard in calculations like these.
    This will VERY marginally improve distance error for Switzerland.
    """
    r = 6367.168  # Radius of Earth in kilometers
    return r * c * 1000  # Convert to meters


# Function to read data from file and add distance column
def add_distance_column(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        header = lines[0].strip().split('\t')
        lines = lines[1:]  # Remove header

        # Find index of latitude and longitude columns
        lat_index = header.index('actualLatitude')
        lon_index = header.index('actualLongitude')
        gps_lat_index = header.index('gpsLatitude')
        gps_lon_index = header.index('gpsLongitude')

        # Calculate distances and add as new columns
        lines = [line.strip().split('\t') for line in lines]
        for line in lines:
            lat1 = float(line[lat_index])
            lon1 = float(line[lon_index])
            lat2 = float(line[gps_lat_index])
            lon2 = float(line[gps_lon_index])

            # Calculate distance between latitudes
            lat_diff = haversine(lat1, lon1, lat2, lon1)

            if lat1 - lat2 < 0:
                """ due to output of haversine formula always being positive, switch mathematical sign if lat2 is lower
                    compared to lat1"""
                lat_diff = -lat_diff

            # Calculate distance between longitudes
            lon_diff = haversine(lat1, lon1, lat1, lon2)

            if lon1 - lon2 < 0:
                """ due to output of haversine formula always being positive, switch mathematical sign if lat2 is more 
                    to the left compared to lat1 """
                lon_diff = -lon_diff

            diff = haversine(lat1, lon1, lat2, lon2)

            # Add distance columns
            line.append(str(lat_diff))
            line.append(str(lon_diff))
            line.append(str(diff))
            print("latDiff: " + str(lat_diff) + " lonDiff: " + str(lon_diff) + " distance: " + str(diff))

        # Update header
        header.extend(['latDifference', 'lonDifference', 'distance'])

        # Write updated data to a new file
        with open('updated_data.csv', 'w') as updated_file:
            updated_file.write('\t'.join(header) + '\n')
            for line in lines:
                updated_file.write('\t'.join(line) + '\n')


add_distance_column(FILE_PATH)
