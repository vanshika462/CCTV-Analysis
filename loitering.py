import cv2
import numpy as np

def detect_loitering(video_path):
    cap = cv2.VideoCapture(video_path)
    
    # Initialize background subtractor
    fg_bg_subtractor = cv2.createBackgroundSubtractorMOG2()

    # Parameters for object tracking
    tracker = cv2.TrackerKCF_create()
    track_objects = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Apply background subtraction
        fg_mask = fg_bg_subtractor.apply(frame)

        # Remove noise and perform morphological operations
        fg_mask = cv2.threshold(fg_mask, 200, 255, cv2.THRESH_BINARY)[1]
        fg_mask = cv2.erode(fg_mask, None, iterations=2)
        fg_mask = cv2.dilate(fg_mask, None, iterations=2)

        # Find contours in the foreground mask
        contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Loop through contours
        for contour in contours:
            # Filter contours based on area (adjust as needed)
            if cv2.contourArea(contour) > 1000:
                # Get bounding box coordinates
                x, y, w, h = cv2.boundingRect(contour)

                # Initialize tracker for new objects
                new_object = True
                for obj in track_objects:
                    _, bbox = obj[0].update(frame)
                    if x > bbox[0] and y > bbox[1] and x + w < bbox[0] + bbox[2] and y + h < bbox[1] + bbox[3]:
                        new_object = False
                        break

                if new_object:
                    tracker = cv2.TrackerKCF_create()
                    tracker.init(frame, (x, y, w, h))
                    track_objects.append((tracker, (x, y, w, h)))

    cap.release()
    cv2.destroyAllWindows()

    # Return the number of people loitering
    return len(track_objects)


