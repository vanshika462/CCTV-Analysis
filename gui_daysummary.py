from pathlib import Path

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame3")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def show_calendar():
    # Create a Tkinter window
    window = tk.Toplevel()
    window.title("Date Selector")

    # Create a Calendar widget
    cal = Calendar(window, selectmode='day', date_pattern='yyyy-mm-dd')
    cal.pack(padx=10, pady=10)

    # Create a button to get the selected date
    button = ttk.Button(window, text="Get Selected Date", command=lambda: get_selected_date(cal,window))
    button.pack(pady=5)

    # Run the Tkinter event loop
    window.mainloop()

def get_selected_date(cal,window):
    selected_date = cal.selection_get()
    messagebox.showinfo("Selected Date", f"You selected: {selected_date}")
    window.destroy()

window = Tk()

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
    command=lambda: print("button_1 clicked"),
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
    command=show_calendar,
    relief="flat"
)
button_2.place(
    x=33.0,
    y=121.0,
    width=165.0,
    height=68.0
)

canvas.create_text(
    25.0,
    33.0,
    anchor="nw",
    text="Day\nSummary",
    fill="#292643",
    font=("LaoSansPro", 20 * -1)
)
window.resizable(False, False)
window.mainloop()
