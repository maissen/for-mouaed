from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from source import *


def main_loader():
    def on_drag(event):
        x = window.winfo_pointerx() - window._offset_x
        y = window.winfo_pointery() - window._offset_y
        window.geometry(f"+{x}+{y}")

    def start_drag(event):
        window._offset_x = event.x
        window._offset_y = event.y

    window = Tk()

    window_width = 630
    window_height = 360

    # Get the screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate the position to center the window
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    window.configure(bg="#FFFFFF")

    # Hide the title bar
    window.overrideredirect(True)

    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=360,
        width=630,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    canvas.create_rectangle(
        0.0,
        0.0,
        630.0,
        360.0,
        fill="#062882",
        outline="")

    canvas.create_rectangle(
        256.0,
        92.0,
        371.0,
        207.0,
        fill="#8E1515",
        outline="")

    canvas.create_text(
        237.0,
        238.0,
        anchor="nw",
        text="Loading",
        fill="#FFFFFF",
        font=("Inter", 36 * -1)
    )

    # Bind mouse events for dragging
    window.bind("<B1-Motion>", on_drag)
    window.bind("<Button-1>", start_drag)
    window.after(1000, lambda: (window.destroy(), load_main_window()))

    window.resizable(False, False)
    window.mainloop()
