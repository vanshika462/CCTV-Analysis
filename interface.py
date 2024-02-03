import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
from count import count_objects
<<<<<<< Updated upstream
=======
from peak_hour import detect_peak_hour
from loitering import detect_loitering
from detecting import layer_names

>>>>>>> Stashed changes

# Placeholder function for activity detection using the model
def detect_activity(input_path, activity_type):
    # Replace this with your actual model code
    # For simplicity, this example just displays a message
    return f"Detecting {activity_type} in {input_path}"

# Function to open a video file or an image file and display the first frame
def open_input():
    file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi"), ("Image files", "*.jpg;*.jpeg;*.png")])
    if file_path:
        cap = cv2.VideoCapture(file_path)

        if not cap.isOpened():
            return

        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img.thumbnail((400, 400))
            img = ImageTk.PhotoImage(img)
            video_label.config(image=img)
            video_label.image = img
            video_label.file_path = file_path

        cap.release()

# Function to perform loitering detection based on the selected option
def loitering_in_input():
    if video_label.file_path:
        exec(open('detecting.py').read())

# Function to count objects in the video or frame
def count_objects_in_input():
    if video_label.file_path:
        object_count = count_objects(video_label.file_path)
        object_count_label.config(text=f"Object Count: {object_count}")

# Function to find peak hour in the total videos
def peak_hour_in_input():
        peak_hour_result = detect_peak_hour()
        peak_hour_label.config(text=f"Peak Hour: {peak_hour_result}")

# Function to count objects in the video or frame
def count_objects_in_input():
    if video_label.file_path:
        object_count = count_objects(video_label.file_path)
        object_count_label.config(text=f"Object Count: {object_count}")

# Main GUI window
root = tk.Tk()
root.title("Activity Detection Interface")

# Video display label
video_label = tk.Label(root)
video_label.pack(pady=10)

# Open Input Button
open_button = tk.Button(root, text="Open File", command=open_input)
open_button.pack(pady=10)

# Count Objects Button
count_objects_button = tk.Button(root, text="Count Objects", command=count_objects_in_input)
count_objects_button.pack(pady=10)
<<<<<<< Updated upstream

# Activity selection
activities = ["Loitering", "Peak Hour Pedestrian Traffic", "Custom Activity"]
activity_var = tk.StringVar(root)
activity_var.set(activities[0])  # Default activity
activity_menu = tk.OptionMenu(root, activity_var, *activities)
activity_menu.pack(pady=10)
=======
>>>>>>> Stashed changes

# Peak Hour Button
peak_hour_button = tk.Button(root, text="Peak Hour", command=peak_hour_in_input)
peak_hour_button.pack(pady=10)

#Loitering Button
loitering_button = tk.Button(root, text="Detecting", command=loitering_in_input)
loitering_button.pack(pady=10)

# Object count label
object_count_label = tk.Label(root, text="Object Count: ")
object_count_label.pack(pady=10)

# Peak hour label
peak_hour_label = tk.Label(root, text="Peak Hour: ")
peak_hour_label.pack(pady=10)

# Loitering count label
#loitering_count_label = tk.Label(root, text="Loitering Count: ")
#loitering_count_label.pack(pady=10)


# # Object count label
# object_count_label = tk.Label(root, text="Object Count: ")
# object_count_label.pack(pady=10)

root.mainloop()
