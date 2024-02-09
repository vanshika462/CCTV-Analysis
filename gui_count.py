from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Frame, Label, filedialog

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def display_selected_frame():
    # Function to be called when the "Select" button is clicked
    # Open a file dialog to let the user select an image
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png;*.gif")])
    
    # If the user selected an image
    if file_path:
        # Create a PhotoImage object from the selected image
        selected_image = PhotoImage(file=file_path)
        
        # Create a Label widget and set the selected image
        selected_label = Label(selected_frame, image=selected_image)
        selected_label.image = selected_image
        selected_label.pack()

window = Tk()

window.geometry("1175x759")
window.configure(bg="#FFFFFF")

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=759,
    width=1175,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    587.0,
    379.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    144.0,
    118.0,
    image=image_image_2
)

canvas.create_text(
    13.0,
    20.0,
    anchor="nw",
    text="         Count",
    fill="#FFFFFF",
    font=("Inter ExtraLight", 28)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=display_selected_frame,
    #command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=21.0,
    y=88.0,
    width=246.1466827392578,
    height=59.61457443237305
)

canvas.create_rectangle(
    285.0,
    -1.0,
    286.00000000000006,
    759.0,
    fill="#BBAAB8",
    outline=""
)

canvas.create_rectangle(
    2.0,
    167.00000011745885,
    291.9999720589767,
    170.0,
    fill="#BBAAB8",
    outline=""
)

selected_frame = Frame(window, width=850, height=500, bg="#BBAAB8")
selected_frame.pack(side="right", padx=20, pady=20)

window.resizable(False, False)
window.mainloop()