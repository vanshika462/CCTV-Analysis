import subprocess
import tkinter as tk
from tkinter import Canvas, Button, PhotoImage, filedialog
from PIL import Image, ImageTk
from pathlib import Path
import cv2
from traffic import *

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

def play_video():
    global cap, video_path
    video_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi")])
    if not video_path:
        return

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

    cap = cv2.VideoCapture(video_path)
    width, height = 441, 291  # Dimensions of image_1
    x, y = 235.0, 18.0  # Coordinates of image_1
    canvas.delete("video")  # Delete any existing video
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (width, height))
        photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        video_image = canvas.create_image(
            x,  # Set x coordinate to the same as image_1
            y,  # Set y coordinate to the same as image_1
            anchor=tk.NW,  # Anchor at the top-left corner
            image=photo,
            tags="video"
        )
        canvas.image = photo  # To prevent garbage collection
        update_video()  # Start updating the video frames

def find_patterns():
    global video_path,entering_count,standing_count,exiting_count
    if video_path:
        entering_count, standing_count, exiting_count=process_video(video_path)
    else:
        print("No video selected.")

def display_traffic_counts():
    global standing_count, exiting_count, entering_count

    # Load the traffic plot image as the background
    plot_path = ASSETS_PATH / "image_2.png"
    plot_image = Image.open(plot_path)
    photo = ImageTk.PhotoImage(plot_image)

    # Display the image as the background
    canvas.delete("video")  # Delete any existing video
    canvas.create_image(
        350.0,  # Set x coordinate
        428.0,  # Set y coordinate
        anchor=tk.CENTER,
        image=photo,
        tags="image_2"
    )
    canvas.image = photo  # To prevent garbage collection

    # Text for entering count
    canvas.create_text(
        350.0,  # Set x coordinate
        390.0,  # Set y coordinate for entering count
        anchor=tk.CENTER,
        text=f"Entering count: {entering_count}",
        fill="#292643",
        font=("LaoSansPro", 12)
    )

    # Text for standing count
    canvas.create_text(
        350.0,  # Set x coordinate
        410.0,  # Set y coordinate for standing count
        anchor=tk.CENTER,
        text=f"Standing count: {standing_count}",
        fill="#292643",
        font=("LaoSansPro", 12)
    )

    # Text for exiting count
    canvas.create_text(
        350.0,  # Set x coordinate
        430.0,  # Set y coordinate for exiting count
        anchor=tk.CENTER,
        text=f"Exiting count: {exiting_count}",
        fill="#292643",
        font=("LaoSansPro", 12)
    )

    # Stop video if it's playing
    stop_video()


window = tk.Tk()

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
    command=find_patterns,
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
