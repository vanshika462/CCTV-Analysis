import cv2
import numpy as np
import csv
import os

def process_video(video_path, output_csv):
    net = cv2.dnn.readNet("darknet\yolov3.weights", "darknet\cfg\yolov3.cfg")
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

    classes = []
    with open("darknet\data\coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]

    cap = cv2.VideoCapture(video_path)
    person_info = {}
    person_id_counter = 1  # Initialize a counter for assigning IDs

    # Get the original video dimensions
    original_width = int(cap.get(3))
    original_height = int(cap.get(4))

    # Create a resizable window
    cv2.namedWindow('Building Entry/Exit', cv2.WINDOW_NORMAL)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        height, width, channels = frame.shape
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

        net.setInput(blob)
        outs = net.forward(output_layers)

        class_ids = []
        confidences = []
        boxes = []

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5 and classes[class_id] == 'person':
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                centroid_x = x + w // 2
                centroid_y = y + h // 2
                person_key = None

                for key, person in person_info.items():
                    px, py, direction, person_id = person
                    distance = np.sqrt((px - centroid_x) ** 2 + (py - centroid_y) ** 2)
                    distance_threshold = 50  # You can adjust this distance threshold

                    if distance < distance_threshold:
                        person_key = key
                        break

                if person_key is None:
                    person_info[person_id_counter] = [centroid_x, centroid_y, None, person_id_counter]
                    person_id_counter += 1
                else:
                    person_info[person_key][0] = centroid_x
                    person_info[person_key][1] = centroid_y

        for key, person in list(person_info.items()):
            px, py, direction, person_id = person
            if direction is None:
                if py < height // 2:
                    person_info[key][2] = "standing"
                elif px < width // 2:
                    person_info[key][2] = "exiting"
                else:
                    person_info[key][2] = "entering"

            if direction != person_info[key][2]:
                # Only write to CSV if the direction changes
                with open(output_csv, "a", newline='') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    if os.path.getsize(output_csv) == 0:  # Check if the file is empty
                        csv_writer.writerow(["Person_ID", "Centroid_X", "Centroid_Y", "Direction"])

                    csv_writer.writerow([person_id, px, py, person_info[key][2]])

                person_info[key][2] = direction

        # Display the processed frame with the original aspect ratio
        cv2.imshow('Building Entry/Exit', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def process_videos(folder_path, output_folder):
    videos = [f for f in os.listdir(folder_path) if f.endswith(".mp4")]

    for video in videos:
        video_path = os.path.join(folder_path, video)
        output_csv = os.path.join(output_folder, f"{os.path.splitext(video)[0]}_output.csv")
        process_video(video_path, output_csv)

# Example usage for processing multiple videos in a folder
videos_folder = "traffic_input"
output_folder = "traffic_output"
process_videos(videos_folder, output_folder)
