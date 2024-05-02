import cv2
import numpy as np
import csv
import os
import pandas as pd

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

    person_info = {}  # Store person ID and last known position
    person_id_counter = 1  # Counter to assign unique IDs to each detected person

    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

    video_name = os.path.splitext(os.path.basename(video_path))[0]
    output_csv = os.path.join(output_folder, f"{video_name}.csv")

    # Write header row to CSV
    with open(output_csv, "w", newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Timestamp", "Person_ID", "Direction", "X_Coordinate", "Y_Coordinate"])

    # Load YOLO
    yolo_weights = "darknet/yolov3.weights"
    yolo_config = "darknet/cfg/yolov3.cfg"
    coco_names = "darknet/data/coco.names"
    if not os.path.isfile(yolo_weights) or not os.path.isfile(yolo_config) or not os.path.isfile(coco_names):
        print("YOLO files not found.")
        return

    net = cv2.dnn.readNet(yolo_weights, yolo_config)
    if net.empty():
        print("Error loading YOLO network.")
        return

    classes = []
    with open(coco_names, "r") as f:
        classes = [line.strip() for line in f.readlines()]

    output_layers = net.getUnconnectedOutLayersNames()
    if not output_layers:
        print("Error retrieving output layers.")
        return

    frame_count = 0  # Counter to keep track of processed frames

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        if frame_count % 5 != 0:  # Process every 5th frame
            continue

        height, width, channels = frame.shape
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

        # Set the input to the YOLO network
        net.setInput(blob)

        # Get the detections
        outs = net.forward(output_layers)

        # Process and draw detections
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5 and class_id == 0:  # Person class_id is 0
                    # Object detected is a person with confidence > 0.5
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                px, py = x + w // 2, y + h // 2

                # Check if the detected person is already in the dictionary
                person_id = None
                for id, info in person_info.items():
                    if abs(px - info['x']) < 100 and abs(py - info['y']) < 100:
                        person_id = id
                        break

                # If the person is not in the dictionary, create a new ID
                if person_id is None:
                    person_id = person_id_counter
                    direction = "standing"
                    person_info[person_id] = {'direction': direction,'x': px, 'y': py}
                    person_id_counter += 1
                    with open(output_csv, 'a', newline='') as csvfile:
                        csv_writer = csv.writer(csvfile)
                        csv_writer.writerow([cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0, person_id, direction, px, py])

                # Determine the direction of the person
                else:
                    y_diff = abs(person_info[person_id]['y'] - py)
                    if py > person_info[person_id]['y'] + 10 and y_diff > 10:
                        direction = "entering"
                    elif py < person_info[person_id]['y'] - 10 and y_diff > 10:
                        direction = "exiting"
                    else:
                        direction = person_info[person_id]['direction']

                    # Update the person's last known position
                    person_info[person_id]['x'] = px
                    person_info[person_id]['y'] = py

                    # Write the entry to the CSV file
                    if direction!=person_info[person_id]['direction']:
                        person_info[person_id]['direction'] = direction
                        with open(output_csv, 'a', newline='') as csvfile:
                            csv_writer = csv.writer(csvfile)
                            csv_writer.writerow([cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0, person_id, direction, px, py])

    cap.release()

    # Analyze the CSV file
    entering_count, standing_count, exiting_count = analyze_single_file(output_csv)
    return entering_count, standing_count, exiting_count
