# import cv2
# import numpy as np

# def count_objects(video_path):
#     net = cv2.dnn.readNet("C:\\Users\\WelCome\\CCTV-Analysis\\darknet\\yolov3.weights", "C:\\Users\\WelCome\\CCTV-Analysis\\darknet\\cfg\\yolov3.cfg")
#     layer_names = net.getLayerNames()
#     output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

#     classes = []
#     with open("darknet\data\coco.names", "r") as f:
#         classes = [line.strip() for line in f.readlines()]

#     cap = cv2.VideoCapture(video_path)
#     object_count = 0

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         height, width, channels = frame.shape
#         blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
#         net.setInput(blob)
#         outs = net.forward(output_layers)

#         # Initialize lists to store bounding boxes, confidences, and class IDs
#         boxes = []
#         confidences = []
#         class_ids = []

#         for out in outs:
#             for detection in out:
#                 scores = detection[5:]
#                 class_id = np.argmax(scores)
#                 confidence = scores[class_id]

#                 if confidence > 0.75:
#                     # Increment object count
#                     object_count += 1

#         cv2.waitKey(1)  # Adjust the waitKey delay if needed

#     cap.release()
#     cv2.destroyAllWindows()

#     return object_count


import cv2
import numpy as np

def count_objects(video_path):
    net = cv2.dnn.readNet("C:\\Users\\WelCome\\CCTV-Analysis\\darknet\\yolov3.weights", "C:\\Users\\WelCome\\CCTV-Analysis\\darknet\\cfg\\yolov3.cfg")
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

    classes = []
    with open("darknet\data\coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]

    cap = cv2.VideoCapture(video_path)
    object_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

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
                    # Increment object count
                    object_count += 1

        cv2.waitKey(1)  # Adjust the waitKey delay if needed

    cap.release()
    cv2.destroyAllWindows()

    return object_count
