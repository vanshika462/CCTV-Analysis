import subprocess
from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("assets/frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def open_script_4():
    window.destroy()  # Close the current window
    subprocess.run(["python", str(OUTPUT_PATH / "gui_patterns.py")])  # Adjust the file name as needed

def open_script_5():
    window.destroy()
    subprocess.run(["python", str(OUTPUT_PATH / "gui_daysummary.py")])  # Adjust the file name as needed

def open_script_6():
    window.destroy()
    subprocess.run(["python", str(OUTPUT_PATH / "gui_count.py")])  

window = Tk()
window.geometry("1235x601")
window.configure(bg="#FFFFFF")
canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=601,
    width=1235,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)
image_image_1 = PhotoImage(file=relative_to_assets("image_4.png"))
canvas.create_image(617.0, 300.0, image=image_image_1)

button_image_1 = PhotoImage(file=relative_to_assets("button_4.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=open_script_4,
    relief="flat"
)
button_1.place(x=910.0, y=339.0, width=281.0, height=95.02040100097656)

button_image_2 = PhotoImage(file=relative_to_assets("button_5.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=open_script_5,
    relief="flat"
)
button_2.place(x=453.0, y=464.0, width=305.0, height=84.0)

button_image_3 = PhotoImage(file=relative_to_assets("button_6.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=open_script_6,
    relief="flat"
)
button_3.place(x=72.0, y=359.0, width=300.0, height=75.29412841796875)

canvas.create_text(
    545.0,
    227.0,
    anchor="nw",
    text="Menu",
    fill="#000000",
    font=("InknutAntiqua Regular", 55 * -1)
)
window.resizable(False, False)
window.mainloop()

