[16:01, 4/12/2024] Sharan College Quantum: import numpy as np
import pandas as pd

def stopping_distance(speed, deceleration=4.5):
    """
    Calculates the stopping distance for a vehicle.

    Parameters:
    - speed: Speed of the vehicle in meters per second (m/s).
    - deceleration: Deceleration rate (default is 4.5 m/s²).

    Returns:
    - Stopping distance in meters.
    """
    return (speed ** 2) / (2 * deceleration)

def distribute_vehicles_randomly_with_gap(total_vehicles, road_length=5000, min_gap=5):
    """
    Distributes vehicles randomly along a road with a minimum gap between them.

    Parameters:
    - total_vehicles: Total number of vehicles.
    - road_length: Length of the road in meters (default is 5 km).
    - min_gap: Minimum gap between two vehicles in meters.

    Returns:
    - List of distances of each vehicle from the starting point.
    """
    vehicle_positions = []
    while len(vehicle_positions) < total_vehicles:
        position = np.random.randint(0, road_length)
        if all(abs(position - pos) >= min_gap for pos in vehicle_positions):
            vehicle_positions.append(position)
    return sorted(vehicle_positions)

def calculate_people_saved(total_vehicles, avg_speed, avg_people_per_vehicle=1.5):
    """
    Estimates the number of people saved during a chain accident.

    Parameters:
    - total_vehicles: Total number of vehicles within 5 km.
    - avg_speed: Average speed of vehicles in km/h.
    - avg_people_per_vehicle: Average number of people per vehicle (default is 1.5).

    Returns:
    - Estimated number of people saved.
    """
    # Convert speed to m/s
    avg_speed_mps = avg_speed * (1000 / 3600)

    # Calculate stopping distance for vehicles
    stop_dist = stopping_distance(avg_speed_mps)

    # Randomly distribute vehicles along the road with a minimum gap
    vehicle_positions = distribute_vehicles_randomly_with_gap(total_vehicles, min_gap=5)

    # Calculate how many vehicles can stop within their stopping distance
    vehicles_able_to_stop = 0
    for i, position in enumerate(vehicle_positions):
        if i == 0 or (position - vehicle_positions[i - 1]) >= stop_dist:
            vehicles_able_to_stop += 1

    # Estimate people saved
    people_saved = vehicles_able_to_stop * avg_people_per_vehicle

    return round(people_saved)

def process_dataset(input_df):
    """
    Processes the input dataset and calculates the number of people saved for each row.

    Parameters:
    - input_df: Pandas DataFrame with columns ['total_vehicles', 'avg_speed'].

    Returns:
    - output_df: Pandas DataFrame with an additional 'people_saved' column.
    """
    output_df = input_df.copy()
    output_df['people_saved'] = output_df.apply(
        lambda row: calculate_people_saved(row['total_vehicles'], row['avg_speed']), axis=1
    )
    return output_df

# Example Usage
# Sample input dataset (you can replace this with your own CSV or data source)
data = {
    'total_vehicles': [100, 150, 200, 50],  # Number of vehicles within 5 km range
    'avg_speed': [80, 60, 100, 40]  # Average speed of vehicles in km/h
}

# Convert the input data into a pandas DataFrame
input_df = pd.DataFrame(data)

# Process the dataset and get the output
output_df = process_dataset(input_df)

# Show the output DataFrame with the 'people_saved' column
print(output_df)
[16:02, 4/12/2024] Sharan College Quantum: take this as a new code
[16:02, 4/12/2024] Sharan College Quantum: only difference is it takes dataset as input and gives dataset as outpuy
[16:02, 4/12/2024] Sharan College Quantum: output*
[16:35, 4/12/2024] Sharan College Quantum: import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Generate random values for 'total_vehicles' (between 1 and 299) and 'avg_speed' (between 30 and 119 km/h)
total_vehicles = np.random.randint(1, 300, size=15)  # 15 random values for total_vehicles (less than 300)
avg_speed = np.random.randint(30, 120, size=15)  # 15 random values for avg_speed (less than 120 km/h)

# Create a DataFrame from the generated data
data = {
    'total_vehicles': total_vehicles,
    'avg_speed': avg_speed
}

# Convert to pandas DataFrame
input_df = pd.DataFrame(data)

# Display the custom input dataset
print(input_df)
input_df.to_csv('custom_vehicle_speed_dataset.csv', index=False)
