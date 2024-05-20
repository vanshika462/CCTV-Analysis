# import cv2
# import os

# def extract_frames_from_videos(video_dir, output_dir):
#     # Create output directory if it doesn't exist
#     os.makedirs(output_dir, exist_ok=True)

#     # Get a list of video files in the directory
#     video_files = [f for f in os.listdir(video_dir) if f.endswith('.mp4')]

#     # Loop over the video files
#     for video_file in video_files:
#         video_path = os.path.join(video_dir, video_file)
#         video_name = os.path.splitext(video_file)[0]
#         frames_output_dir = os.path.join(output_dir, video_name)

#         # Create a directory for the frames of this video
#         os.makedirs(frames_output_dir, exist_ok=True)

#         # Open the video file
#         cap = cv2.VideoCapture(video_path)
#         frame_count = 0

#         while cap.isOpened():
#             # Read the frame from the video
#             ret, frame = cap.read()

#             if not ret:
#                 break

#             # Save the frame as an image
#             frame_filename = f"frame_{frame_count:04d}.jpg"
#             frame_path = os.path.join(frames_output_dir, frame_filename)
#             cv2.imwrite(frame_path, frame)

#             frame_count += 1

#         cap.release()

# # Specify the directory containing the input video files
# video_dir = 'dummy_vids'

# # Specify the output directory where the frames will be saved
# output_dir = 'frames'

# # Call the function to extract frames from the videos
# extract_frames_from_videos(video_dir, output_dir)

import cv2
import os
import numpy as np

def load_yolo():
    net = cv2.dnn.readNet("darknet\yolov3.weights", "darknet\cfg\yolov3.cfg")
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    with open("darknet\data\coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]
    return net, classes, output_layers

def detect_objects(frame, net, output_layers):
    height, width, _ = frame.shape
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)
    return outs, width, height

def process_detection(outs, width, height, classes, confidence_threshold=0.5, nms_threshold=0.4):
    class_ids, confidences, boxes = [], [], []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > confidence_threshold:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
    indices = cv2.dnn.NMSBoxes(boxes, confidences, confidence_threshold, nms_threshold)
    return indices, boxes, class_ids, confidences

def draw_labels(indices, boxes, class_ids, confidences, classes, frame):
    for i in indices:
        i = i[0]
        box = boxes[i]
        x, y, w, h = box
        label = str(classes[class_ids[i]])
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, f"{label} {confidences[i]:.2f}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return frame

def extract_frames_from_videos(video_dir, output_dir, net, classes, output_layers):
    os.makedirs(output_dir, exist_ok=True)
    video_files = [f for f in os.listdir(video_dir) if f.endswith('.mp4')]

    for video_file in video_files:
        video_path = os.path.join(video_dir, video_file)
        frames_output_dir = os.path.join(output_dir, os.path.splitext(video_file)[0])
        os.makedirs(frames_output_dir, exist_ok=True)
        cap = cv2.VideoCapture(video_path)
        frame_count = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            outs, width, height = detect_objects(frame, net, output_layers)
            indices, boxes, class_ids, confidences = process_detection(outs, width, height, classes)
            frame = draw_labels(indices, boxes, class_ids, confidences, classes, frame)
            frame_filename = f"frame_{frame_count:04d}.jpg"
            frame_path = os.path.join(frames_output_dir, frame_filename)
            cv2.imwrite(frame_path, frame)
            frame_count += 1
        cap.release()

# Load YOLO
net, classes, output_layers = load_yolo()

# Specify directories
video_dir = 'dummy_vids'
output_dir = 'frames'

# Extract frames and detect objects
extract_frames_from_videos(video_dir, output_dir, net, classes, output_layers)

