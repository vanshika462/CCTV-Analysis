import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
from count import count_objects

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

# Function to perform activity detection based on the selected option
def detect_selected_activity():
    if video_label.file_path:
        selected_activity = activity_var.get()
        result = detect_activity(video_label.file_path, selected_activity)
        result_label.config(text=result)

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

# Activity selection
activities = ["Loitering", "Peak Hour Pedestrian Traffic", "Custom Activity"]
activity_var = tk.StringVar(root)
activity_var.set(activities[0])  # Default activity
activity_menu = tk.OptionMenu(root, activity_var, *activities)
activity_menu.pack(pady=10)

# Detect Activity Button
detect_button = tk.Button(root, text="Detect Activity", command=detect_selected_activity)
detect_button.pack(pady=10)

# Result label
result_label = tk.Label(root, text="")
result_label.pack(pady=10)

# Object count label
object_count_label = tk.Label(root, text="Object Count: ")
object_count_label.pack(pady=10)

root.mainloop()
