import tkinter as tk
from tkinter import Canvas, Button, PhotoImage, filedialog
from PIL import Image, ImageTk
from pathlib import Path
import cv2

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\vansh\Desktop\Projects\CCTV-Analysis\interface\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

cap = None  # Global variable to hold the video capture object

def play_video():
    global cap
    file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi")])
    if not file_path:
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

    cap = cv2.VideoCapture(file_path)
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

def display_traffic_plot():
    # Load the traffic plot image
    plot_path = ASSETS_PATH / "traffic_plot.png"
    plot_image = Image.open(plot_path)

    # Resize the plot image to match the size of image_2
    target_width = 455
    target_height = 163
    plot_image = plot_image.resize((target_width, target_height))
    # Display the plot image in place of image_2
    photo = ImageTk.PhotoImage(plot_image)
    canvas.delete("video")  # Delete any existing video
    canvas.create_image(
        350.0,  # Set x coordinate to the same as image_2
        428.0,  # Set y coordinate to the same as image_2
        anchor=tk.CENTER,
        image=photo,
        tags="image_2"
    )
    canvas.image = photo  # To prevent garbage collection

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

button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
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
    command=display_traffic_plot,
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
