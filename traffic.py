import cv2
import numpy as np
import csv
import os
import pandas as pd
import matplotlib.pyplot as plt

# Function to analyze a single CSV file
def analyze_single_file(file_path):
    # Read CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Count the number of people entering, standing, and exiting
    entering_count = df[df['Direction'] == 'entering'].shape[0]
    standing_count = df[df['Direction'] == 'standing'].shape[0]
    exiting_count = df[df['Direction'] == 'exiting'].shape[0]

    return entering_count, standing_count, exiting_count


def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    output_folder = "traffic_output"

    if not cap.isOpened():
        print(f"Error opening video file: {video_path}")
        return

    background_subtractor = cv2.createBackgroundSubtractorMOG2()

    person_info = {}

    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

    video_name = os.path.splitext(os.path.basename(video_path))[0]
    output_csv = os.path.join(output_folder, f"{video_name}.csv")

    # Open the CSV file in 'w' mode to write the header row
    with open(output_csv, "w", newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Timestamp", "Person_ID", "Direction", "Centroid_X", "Centroid_Y"])

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        mask = background_subtractor.apply(frame)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            contour = contours[0]
            x, y, w, h = cv2.boundingRect(contour)
            px, py = x + w // 2, y + h // 2

            person_id = 1

            if person_id not in person_info:
                person_info[person_id] = {"direction": None, "last_entry_time": None}

            if person_info[person_id]["last_entry_time"] is None:
                timestamp = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0

                with open(output_csv, "a", newline='') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow([timestamp, person_id, "standing", px, py])

                person_info[person_id]["last_entry_time"] = timestamp

            else:
                direction = "entering" if py > height // 2 else "exiting"

                if direction != person_info[person_id]["direction"]:
                    timestamp = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0

                    with open(output_csv, "a", newline='') as csvfile:
                        csv_writer = csv.writer(csvfile)
                        csv_writer.writerow([timestamp, person_id, direction, px, py])

                    person_info[person_id]["direction"] = direction

    cap.release()

    entering_count, standing_count, exiting_count = analyze_single_file(output_csv)
    return entering_count, standing_count, exiting_count

