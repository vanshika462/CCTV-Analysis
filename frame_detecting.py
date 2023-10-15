import numpy as np
import cv2
import os
import tensorflow as tf

# Load the YOLO3 model
model = tf.keras.models.load_model('yolov3_model.h5')

# Define class labels (modify based on your YOLO3 model's class labels)
class_labels = ["person", "car", "bicycle", "motorbike", "truck"]

# Constants for YOLO3 output
NUM_CLASSES = len(class_labels)
NUM_ANCHORS = 9
GRID_SIZE = 13  # Change this according to your YOLO3 model

# Function to parse YOLO3 detection results
def parse_yolo3_output(output_tensor):
    # (Parse logic as described in the previous answers)
    # ...

# Path to the folder containing frame images
    frame_folder = 'frames/ch4_20230824153939/'


# Path to the folder where you want to save the detection results
output_folder = 'output_frames/ch4_20230824153939/'

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Process each frame in the input folder
for filename in os.listdir(frame_folder):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        frame_path = os.path.join(frame_folder, filename)
        frame = cv2.imread(frame_path)

        # Preprocess the frame (resize, normalize, etc.) as needed for your YOLO3 model
        frame = preprocess_frame(frame)

        # Run object detection on the preprocessed frame
        detections = model.predict(np.expand_dims(frame, axis=0))

        # Parse detection results for this frame
        bx, by, bw, bh, predicted_class, confidence_scores = parse_yolo3_output(detections)

        # Optionally, filter and process the detection results for this frame

        # Display the results or take further actions (e.g., drawing bounding boxes)
        # ...

        # Save the frame with detection results to the output folder
        output_path = os.path.join(output_folder, filename)
        cv2.imwrite(output_path, frame)

# Release any resources if necessary
# ...

print("Processing completed.")
