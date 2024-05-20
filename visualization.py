import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Function to read and concatenate CSV files from a folder
def read_csv_files(folder_path):
    dfs = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)
            df = pd.read_csv(file_path)
            # Extract time from the filename
            time = filename[-10:-4]  # Extract the last 6 characters representing time
            # Add time as a column in the DataFrame
            df['Time'] = time
            dfs.append(df)
    return pd.concat(dfs, ignore_index=True)

# Function to count entering and exiting people
def count_entering_exiting_people(df):
    # Group by time and count the number of entries for each direction
    counts = df.groupby(['Time', 'Direction']).size().unstack(fill_value=0)
    return counts

# Specify the folder containing CSV files
input_folder = 'traffic_output\Aug23'

# Read CSV files into a DataFrame
data = read_csv_files(input_folder)

# Count entering and exiting people
counts = count_entering_exiting_people(data)
net_count = counts['entered'].sum() - counts['exiting'].sum()

# Plotting
plt.figure(figsize=(10, 6))

# Get the unique times for x-axis ticks
times = sorted(counts.index)

# Convert time strings to datetime objects
times = [datetime.strptime(time, "%H%M%S") for time in times]

# Plot entering people
plt.plot(times, counts['entering'], label='Entering', marker='o')

# Plot exiting people
plt.plot(times, counts['exiting'], label='Exiting', marker='o')

plt.title('Count of Entering and Exiting People in the building over Time')
plt.xlabel('Time')
plt.ylabel('Count')
plt.legend()
plt.xticks(rotation=45)  # Rotate x-axis labels for better visibility
plt.grid(True)
plt.tight_layout()

# Save the plot as an image
output_path = r'C:\Users\vansh\Desktop\Projects\CCTV-Analysis\assets\frame3'
os.makedirs(output_path, exist_ok=True)  # Create the directory if it doesn't exist
plt.savefig(os.path.join(output_path, '2024-04-19.png'))

plt.show()
print("Net count of people entered minus the total number of people exited:", net_count)

