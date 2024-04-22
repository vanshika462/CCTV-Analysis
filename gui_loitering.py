import tkinter as tk
from tkinter import Canvas, Button, PhotoImage, filedialog
from PIL import Image, ImageTk
from pathlib import Path
import cv2
import subprocess


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\vansh\Desktop\Projects\CCTV-Analysis\assets\frame2")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

cap = None  # Global variable to hold the video capture object

def play_video():
    global cap
    file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi")])
    if not file_path:
        return

    subprocess.Popen(["python", "loitering.py", "--video_path", file_path])

window = tk.Tk()

window.geometry("700x550")
window.configure(bg = "#BBAAB8")


canvas = Canvas(
    window,
    bg = "#BBAAB8",
    height = 550,
    width = 700,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
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

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=play_video,  # Change command to call play_video function
    relief="flat"
)
button_1.place(
    x=33.0,
    y=200.0,
    width=165.0,
    height=68.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),  # Placeholder command
    relief="flat"
)
button_2.place(
    x=33.0,
    y=116.0,
    width=165.0,
    height=61.0
)

canvas.create_text(
    33.0,
    25.0,
    anchor="nw",
    text="Loitering\nCount",
    fill="#292643",
    font=("LaoSansPro", 20 * -1)
)
window.resizable(False, False)
window.mainloop()
