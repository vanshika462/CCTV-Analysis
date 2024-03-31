from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Frame, Label, filedialog
from PIL import ImageFilter, ImageTk, Image

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame1")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def display_selected_frame():
    # Function to be called when the "Select" button is clicked
    # Open a file dialog to let the user select an image
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png;*.gif")])
    
    # If the user selected an image
    if file_path:
        # Open the image using Pillow
        original_image = Image.open(file_path)
        
        # Resize the image to fit within the 850x500 rectangle while maintaining aspect ratio
        width, height = original_image.size
        aspect_ratio = height / width
        new_width = 850
        new_height = int(new_width * aspect_ratio)
        resized_image = original_image.resize((new_width, new_height), Image.BICUBIC)
        
        # Convert the resized image to a PhotoImage object
        resized_photo = ImageTk.PhotoImage(resized_image)
        
        # Create a Label widget and set the resized image
        selected_label = Label(selected_frame, image=resized_photo)
        selected_label.image = resized_photo
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
    text="        Count",
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
    relief="flat",
    bg="#B3A3B3" 
)
button_1.place(
    x=21.0,
    y=88.0,
    width=246.1466827392578,
    height=59.61457443237305
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat",
    bg="#A799AC" 
)
button_2.place(
    x=21.0,
    y=200.0,
    width=246.1466827392578,
    height=59.61457443237305
)

canvas.create_rectangle(
    36.0,
    290.0,
    257.0,
    630.0,
    fill="#BBAAB8",
    outline="")

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