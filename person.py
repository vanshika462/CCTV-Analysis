import cv2
import numpy as np

# Load YOLO model and class names
net = cv2.dnn.readNet("darknet\yolov3.weights", "darknet\cfg\yolov3.cfg")
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# Load class names
classes = []
with open("darknet\data\coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Initialize video capture (use your video source or file)
cap = cv2.VideoCapture('dummy_vids\ch4_20230824153939.mp4')

# Initialize a list to store person centroids and directions
person_info = []

# Define a file name to save the data
output_file = "person_info.txt"

# Create a resizable window
cv2.namedWindow("Building Entry/Exit", cv2.WINDOW_NORMAL)

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
            if confidence > 0.5 and classes[class_id] == 'person':
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

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            centroid_x = x + w // 2
            centroid_y = y + h // 2

            # Check if this is a new person or an existing one
            new_person = True
            for person in person_info:
                px, py, direction = person
                distance = np.sqrt((px - centroid_x) ** 2 + (py - centroid_y) ** 2)
                distance_threshold = 50  # You can adjust this distance threshold
                if distance < distance_threshold:
                    # Update the existing person's position
                    person[0] = centroid_x
                    person[1] = centroid_y
                    new_person = False
                    break

            if new_person:
                person_info.append([centroid_x, centroid_y, None])

    # Determine the direction of movement for each person
    for i in range(len(person_info)):
        px, py, direction = person_info[i]
        if direction is None:
            if px < width // 2:
                person_info[i][2] = "exiting"
            else:
                person_info[i][2] = "entering"
                print("Person has exited the building")

    # Save person_info to a text file
    with open(output_file, "w") as f:
        for px, py, direction in person_info:
            f.write(f"Centroid: ({px}, {py}), Direction: {direction}\n")

    # Display the processed frame with the original aspect ratio
    cv2.imshow("Building Entry/Exit", cv2.resize(frame, (800, 600)))

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
