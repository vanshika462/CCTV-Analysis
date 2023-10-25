import cv2
import numpy as np

# Create background subtractor
fgbg = cv2.createBackgroundSubtractorMOG2()
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
min_contour_area = 500

def visualize_walking_model(video_path):
    cap = cv2.VideoCapture(video_path)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        fgmask = fgbg.apply(frame)
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
        
        contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_area]
        
        frame_with_contours = frame.copy()
        
        for contour in filtered_contours:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame_with_contours, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            M = cv2.moments(contour)
            centroid_x = int(M["m10"] / M["m00"])
            centroid_y = int(M["m01"] / M["m00"])
            cv2.circle(frame_with_contours, (centroid_x, centroid_y), 5, (0, 0, 255), -1)
            
        cv2.imshow('Walking Model', frame_with_contours)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

# Specify the path to your video file
video_path = r'dummy_vids\ch4_20230824164857.mp4'

# Call the function to visualize the walking model
visualize_walking_model(video_path)
