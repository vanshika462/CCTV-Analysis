import cv2
import numpy as np
import csv
import os

def process_video(video_path, output_csv):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Error opening video file: {video_path}")
        return

    background_subtractor = cv2.createBackgroundSubtractorMOG2()

    person_info = {}

    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

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

def process_videos(folder_path, output_folder):
    videos = [f for f in os.listdir(folder_path) if f.endswith(".mp4")]

    for video in videos:
        video_path = os.path.join(folder_path, video)
        output_csv = os.path.join(output_folder, f"{os.path.splitext(video)[0]}_output.csv")

        print(f"Processing video: {video}")
        print(f"Output CSV: {output_csv}")

        process_video(video_path, output_csv)

# Example usage for processing multiple videos in a folder
videos_folder = "traffic_input"
output_folder = "traffic_output"

print(f"Videos folder: {videos_folder}")
print(f"Output folder: {output_folder}")

process_videos(videos_folder, output_folder)
