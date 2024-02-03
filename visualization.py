<<<<<<< Updated upstream
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function to read and concatenate CSV files from a folder
def read_csv_files(folder_path):
    dfs = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)
            df = pd.read_csv(file_path)
            dfs.append(df)
    return pd.concat(dfs, ignore_index=True)

# Function to create visualizations
def create_movement_visualizations(df):
    plt.figure(figsize=(14, 8))

    # Print column names for inspection
    print("Column Names:", df.columns)

    # Plotting Timestamp vs Centroid_X and Centroid_Y
    plt.subplot(2, 2, 1)
    sns.lineplot(x='Timestamp', y='Centroid_X', data=df, label='Centroid_X')
    sns.lineplot(x='Timestamp', y='Centroid_Y', data=df, label='Centroid_Y')
    plt.title('Centroid_X and Centroid_Y over Time')
    plt.xlabel('Timestamp')
    plt.ylabel('Centroid')

    # Plotting Direction over Time
    plt.subplot(2, 2, 2)
    sns.lineplot(x='Timestamp', y='Direction', data=df)
    plt.title('Direction over Time')
    plt.xlabel('Timestamp')
    plt.ylabel('Direction')

    # Scatter plot of Centroid_X vs Centroid_Y
    plt.subplot(2, 2, 3)
    sns.scatterplot(x='Centroid_X', y='Centroid_Y', data=df, hue='Direction')
    plt.title('Scatter Plot of Centroid_X vs Centroid_Y')
    plt.xlabel('Centroid_X')
    plt.ylabel('Centroid_Y')
    plt.legend()

    plt.tight_layout()
    plt.show()

# Specify the folder containing CSV files
input_folder = 'traffic_output'

# Read CSV files into a DataFrame
data = read_csv_files(input_folder)

# Create visualizations
create_movement_visualizations(data)
=======
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function to read and concatenate CSV files from a folder
def read_csv_files(folder_path):
    dfs = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)
            df = pd.read_csv(file_path)
            dfs.append(df)
    return pd.concat(dfs, ignore_index=True)

# Function to create visualizations
def create_movement_visualizations(df):
    plt.figure(figsize=(14, 8))

    # Print column names for inspection
    print("Column Names:", df.columns)

    # Plotting Timestamp vs Centroid_X and Centroid_Y
    plt.subplot(2, 2, 1)
    sns.lineplot(x='Timestamp', y='Centroid_X', data=df, label='Centroid_X')
    sns.lineplot(x='Timestamp', y='Centroid_Y', data=df, label='Centroid_Y')
    plt.title('Centroid_X and Centroid_Y over Time')
    plt.xlabel('Timestamp')
    plt.ylabel('Centroid')

    # Plotting Direction over Time
    plt.subplot(2, 2, 2)
    sns.lineplot(x='Timestamp', y='Direction', data=df)
    plt.title('Direction over Time')
    plt.xlabel('Timestamp')
    plt.ylabel('Direction')

    # Scatter plot of Centroid_X vs Centroid_Y
    plt.subplot(2, 2, 3)
    sns.scatterplot(x='Centroid_X', y='Centroid_Y', data=df, hue='Direction')
    plt.title('Scatter Plot of Centroid_X vs Centroid_Y')
    plt.xlabel('Centroid_X')
    plt.ylabel('Centroid_Y')
    plt.legend()

    plt.tight_layout()
    plt.show()

# Specify the folder containing CSV files
input_folder = 'traffic_output'

# Read CSV files into a DataFrame
data = read_csv_files(input_folder)

# Create visualizations
create_movement_visualizations(data)
>>>>>>> Stashed changes
