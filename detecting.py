import cv2
import numpy as np

# Load YOLO model and class names
net = cv2.dnn.readNet("darknet\yolov3.weights","darknet\cfg\yolov3.cfg")
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# Load class names
classes = []
with open("darknet\data\coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Initialize video capture (use your video source or file)
cap = cv2.VideoCapture('dummy_vids\ch4_20230824164618.mp4')

# Get the original video dimensions
original_width = int(cap.get(3))
original_height = int(cap.get(4))

# Create a resizable window
cv2.namedWindow("Vehicle Detection", cv2.WINDOW_NORMAL)

while True:
    # Read frames from a video
    ret, frame = cap.read()
    if not ret:
        break

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
            if confidence > 0.5:
                # Object detected
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
            label = str(classes[class_ids[i]])
            confidence = confidences[i]
            color = (0, 255, 0)  # Green color for the bounding box

            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, f"{label} {confidence:.2f}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # Display the processed frame with the original aspect ratio
    cv2.imshow("Vehicle Detection", frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
