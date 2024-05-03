import subprocess
import tkinter as MovementPatterns
from tkinter import Canvas, Button, PhotoImage, filedialog
from PIL import Image, ImageTk
from pathlib import Path
import cv2
from traffic import *
import time
import os
import threading

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame1")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def open_script_1():
    window.destroy()  # Close the current window
    subprocess.run(["python", str(OUTPUT_PATH / "menu_gui.py")])  # Adjust the file name as needed

cap = None  # Global variable to hold the video capture object
video_path = None  # Global variable to hold the selected video path
entering_count = None
standing_count = None
exiting_count = None
csv_content = ""

def play_video():
    global cap, video_path
    video_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi")])
    if not video_path:
        return

    cap = cv2.VideoCapture(video_path)
    width, height = 441, 291  # Dimensions of image_1
    x, y = 235.0, 18.0  # Coordinates of image_1
    canvas.delete("video")  # Delete any existing video
    canvas.delete("count_text")

    def update_video():
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (width, height))
            photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            canvas.itemconfig(video_image, image=photo)
            canvas.image = photo  # To prevent garbage collection
            canvas.after(10, update_video)  # Update video every 10 milliseconds
        else:
            cap.release()

    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (width, height))
        photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        video_image = canvas.create_image(
            x,  # Set x coordinate to the same as image_1
            y,  # Set y coordinate to the same as image_1
            anchor=MovementPatterns.NW,  # Anchor at the top-left corner
            image=photo,
            tags="video"
        )
        canvas.image = photo  # To prevent garbage collection
        update_video()  # Start updating the video frames

def button_2_command():
    threading.Thread(target=find_patterns_and_display_csv).start()

def find_patterns_and_display_csv():
    global video_path, entering_count, standing_count, exiting_count, csv_content
    if video_path:
        # Extract the base name of the video file
        video_name = os.path.splitext(os.path.basename(video_path))[0]
        # Construct the CSV file path with the same name as the video file
        csv_file_path = f"traffic_output/Aug23/{video_name}.csv"
        # Update image_2 frame with CSV content
        if os.path.exists(csv_file_path):
            # Find counts
            entering_count, standing_count, exiting_count = analyze_single_file(csv_file_path)
            # If the CSV file exists, read its content
            with open(csv_file_path, "r") as file:
                csv_content = file.read()
        else:
            # If the CSV file does not exist, analyze the video
            entering_count, standing_count, exiting_count = process_video(video_path)
            # Save the CSV content to the file
            with open(csv_file_path, "r") as file:
                csv_content = file.read()
    else:
        print("No video selected.")
    display_csv_content()

def display_csv_content():
    global csv_content
    # Load the traffic plot image as the background
    plot_path = ASSETS_PATH / "image_2.png"
    plot_image = Image.open(plot_path)
    photo = ImageTk.PhotoImage(plot_image)

    canvas.create_image(
        350.0,  # Set x coordinate
        428.0,  # Set y coordinate
        anchor=MovementPatterns.CENTER,
        image=photo,
        tags="count_text"
    )
    canvas.image = photo  # To prevent garbage collection

    # Text for CSV content
    canvas.create_text(
        350.0,  # Set x coordinate
        400.0,  # Set y coordinate for CSV content
        anchor=MovementPatterns.CENTER,
        text=csv_content,
        fill="#292643",
        font=("LaoSansPro", 12),
        tags="count_text"
    )

def display_traffic_counts():
    global standing_count, exiting_count, entering_count

    # Delete only the traffic count text, keeping the video display intact
    canvas.delete("count_text")

    # Text for entering count
    canvas.create_text(
        350.0,  # Set x coordinate
        390.0,  # Set y coordinate for entering count
        anchor=MovementPatterns.CENTER,
        text=f"Entering count: {entering_count}",
        fill="#292643",
        font=("LaoSansPro", 12),
        tags="count_text"
    )

    # Text for standing count
    canvas.create_text(
        350.0,  # Set x coordinate
        410.0,  # Set y coordinate for standing count
        anchor=MovementPatterns.CENTER,
        text=f"Entered count: {standing_count}",
        fill="#292643",
        font=("LaoSansPro", 12),
        tags="count_text"
    )

    # Text for exiting count
    canvas.create_text(
        350.0,  # Set x coordinate
        430.0,  # Set y coordinate for exiting count
        anchor=MovementPatterns.CENTER,
        text=f"Exiting count: {exiting_count}",
        fill="#292643",
        font=("LaoSansPro", 12),
        tags="count_text"
    )

window = MovementPatterns.Tk()

window.geometry("700x550")
window.configure(bg="#BBAAB8")

canvas = Canvas(
    window,
    bg="#BBAAB8",
    height=550,
    width=700,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    455.0,
    163.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    350.0,
    428.0,
    image=image_image_2
)

button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=display_traffic_counts,
    relief="flat"
)
button_1.place(
    x=33.0,
    y=240.0,
    width=165.0,
    height=69.0
)

button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=button_2_command,
    relief="flat"
)
button_2.place(
    x=33.0,
    y=163.0,
    width=165.0,
    height=68.0
)

button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=play_video,
    relief="flat"
)
button_3.place(
    x=33.0,
    y=93.0,
    width=165.0,
    height=61.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("back_button.png"))
button_4= Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=open_script_1,
    relief="flat",
    bg="#A799AC" 
)
button_4.config(width=20, height=20)  # Set the width and height to a smaller value
button_4.place(
    x=679,  
    y=4,
    width=15,
    height=15
)

canvas.create_text(
    33.0,
    25.0,
    anchor="nw",
    text="Movement Patterns",
    fill="#292643",
    font=("LaoSansPro", 20 * -1)
)
window.resizable(False, False)
window.mainloop()
