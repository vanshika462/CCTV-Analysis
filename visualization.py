import os
import pandas as pd
import matplotlib.pyplot as plt

# Function to read and concatenate CSV files from a folder
def read_csv_files(folder_path):
    dfs = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)
            df = pd.read_csv(file_path)
            dfs.append(df)
    return pd.concat(dfs, ignore_index=True)

# Function to count entering and exiting people
def count_entering_exiting_people(df):
    # Group by timestamp and count the number of entries for each direction
    counts = df.groupby(['Timestamp', 'Direction']).size().unstack(fill_value=0)
    return counts

# Specify the folder containing CSV files
input_folder = 'traffic_output\Apr24'

# Read CSV files into a DataFrame
data = read_csv_files(input_folder)

# Count entering and exiting people
counts = count_entering_exiting_people(data)

# Plotting
plt.figure(figsize=(10, 6))

# Plot entering people
plt.plot(counts.index, counts['entering'], label='Entering', marker='o')

# Plot exiting people
plt.plot(counts.index, counts['exiting'], label='Exiting', marker='o')

plt.title('Count of Entering and Exiting People over Time')
plt.xlabel('Timestamp')
plt.ylabel('Count')
plt.legend()
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()

# Save the plot as an image
output_path = r'C:\Users\vansh\Desktop\Projects\CCTV-Analysis\assets\frame3'
os.makedirs(output_path, exist_ok=True)  # Create the directory if it doesn't exist
plt.savefig(os.path.join(output_path, '2024-04-19.png'))

plt.show()
