import subprocess
from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("assets/frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def open_second_window():
    # Close the first window
    window.destroy()
    
    # Path to the second script
    script_path = OUTPUT_PATH / "menu_gui.py"
    
    # Run the second script
    subprocess.run(["python", script_path])

# First Window
window = Tk()
window.geometry("1099x595")
window.configure(bg="#FFFFFF")
canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=595,
    width=1099,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)
image_image_1 = PhotoImage(file=relative_to_assets("image_3.png"))
canvas.create_image(549.0, 315.0, image=image_image_1)
button_image_1 = PhotoImage(file=relative_to_assets("button_3.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=open_second_window,  # Modified command
    relief="flat"
)
button_1.place(x=77.0, y=372.0, width=227.3, height=57.2)
window.mainloop()
