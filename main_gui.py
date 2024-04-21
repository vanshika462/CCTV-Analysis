from pathlib import Path

from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets/frame0/")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("1099x595")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 595,
    width = 1099,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_1 = canvas.create_image(
    549.0,
    315.0,
    image=image_image_1
)

canvas.create_text(
    90.0,
    287.0,
    anchor="nw",
    text="Welcome!",
    fill="#FFFFFF",
    font=("InriaSans Regular", 45 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat"
)
button_1.place(
    x=77.0,
    y=372.0,
    width=227.32672119140625,
    height=57.166664123535156
)
window.resizable(False, False)
window.mainloop()
