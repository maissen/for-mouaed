import tkinter as tk
from tkinter import ttk

def popup_message(title, message):
    # Create the popup window
    popup = tk.Tk()
    popup.title(title)
    popup_width = 350
    popup_height = 80

    # Get the screen width and height
    screen_width = popup.winfo_screenwidth()
    screen_height = popup.winfo_screenheight()

    # Calculate the position of the popup window to center it on the screen
    x = (screen_width - popup_width) // 2
    y = (screen_height - popup_height) // 2

    # Set the geometry of the popup window
    popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")

    # Create and pack the label
    label = ttk.Label(popup, text=message)
    label.pack(pady=20)

    # Schedule the closing of the popup after 3500 milliseconds (3.5 seconds)
    popup.after(3500, popup.destroy)

popup_message("title", "message")
