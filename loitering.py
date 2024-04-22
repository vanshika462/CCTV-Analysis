import cv2
import torch
from pathlib import Path
import time
from yolov5.models.experimental import attempt_load
from yolov5.utils.augmentations import letterbox
from yolov5.utils.general import non_max_suppression, scale_coords
from yolov5.utils.plots import plot_one_box

# Load YOLOv5 model
weights = 'yolov5s.pt'  # Or other YOLOv5 weights file
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
model = attempt_load(weights, map_location=device)

# Set video input
video_path = 'dummy_vids\ch4_20230824151107.mp4'
cap = cv2.VideoCapture(video_path)

# Set parameters
loitering_time_threshold = 10  # Time threshold in seconds
person_id = 0  # Class ID for person detection in YOLOv5

# Initialize variables
start_time = None
loitering_detected = False

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Perform detection
    img = letterbox(frame, new_shape=model.img_size)[0]
    img = img[:, :, ::-1].transpose(2, 0, 1)
    img = torch.from_numpy(img).to(device)
    img /= 255.0
    if img.ndimension() == 3:
        img = img.unsqueeze(0)

    # Inference
    pred = model(img)[0]

    # Apply NMS
    pred = non_max_suppression(pred, 0.4, 0.5)

    for det in pred[0]:
        if det is not None and det[-1] == person_id:
            bbox = det[:4].cpu().numpy()
            bbox = scale_coords(img.shape[2:], bbox, frame.shape).astype(int)
            x1, y1, x2, y2 = bbox

            # Draw bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Track time spent in frame
            if start_time is None:
                start_time = time.time()
            else:
                elapsed_time = time.time() - start_time
                if elapsed_time >= loitering_time_threshold:
                    loitering_detected = True
                    # Trigger alert or take action

    if loitering_detected:
        cv2.putText(frame, "Loitering Detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow('Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
