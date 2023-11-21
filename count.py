import cv2
import numpy as np

net = cv2.dnn.readNet("C:\\Users\\WelCome\\CCTV-Analysis\\darknet\\yolov3.weights", "C:\\Users\\WelCome\\CCTV-Analysis\\darknet\\cfg\\yolov3.cfg")
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

classes = []
with open("darknet\data\coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Read a single frame (replace 'your_frame_path.jpg' with the actual path)
frame = cv2.imread('C:\\Users\\WelCome\\CCTV-Analysis\\frames\\ch4_20230824164618\\frame_0255.jpg')

height, width, channels = frame.shape
blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

net.setInput(blob)
outs = net.forward(output_layers)

# Initialize lists to store bounding boxes, confidences, and class IDs
boxes = []
confidences = []
class_ids = []

for out in outs:
    for detection in out:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]

        if confidence > 0.75:
            # Scale the bounding box back to the original image size
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

# Apply Non-Maximum Suppression (NMS)
indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

# Initialize dictionary to store label counts for the current frame
label_counts = {class_name: 0 for class_name in classes}

# Process and draw filtered detections
for i in range(len(boxes)):
    if i in indexes:
        x, y, w, h = boxes[i]
        label = str(classes[class_ids[i]])
        confidence = confidences[i]

        # Update class count
        label_counts[label] += 1

        color = (0, 255, 0)  # Green color for the bounding box
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        cv2.putText(frame, f"{label} {confidence:.2f}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

# Print the label counts for the current frame
for class_name, count in label_counts.items():
    if count > 0:
        print(f"{class_name}: {count} instances detected")

# Display the processed frame
cv2.imshow("Object Detection", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()

