from tkinter import Tk, Canvas, Entry, Button, Text, Scrollbar, Frame, Label
from tkinter.ttk import Combobox
import tkinter as tk
import pickle
import webbrowser
from my_functions import *
import feedparser




def load_main_window():
    create_variables()
    window = Tk()

    window_width = 1250
    window_height = 670

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x_coordinate = (screen_width - window_width) // 2
    y_coordinate = (screen_height - window_height) // 2

    window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
    window.configure(bg="#000")

    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=670,
        width=1250,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    # red rectangle
    canvas.place(x=0, y=0)
    canvas.create_rectangle(
        174.0,
        0.0,
        1250.0,
        670.0,
        fill="#d9d9d9",
        outline=""
    )

    # navbar 
    canvas.create_rectangle(
        0.0,
        0.0,
        174.0,
        670.0,
        fill="#000",
        outline=""
    )

    sources_btn = Button(
        window,
        text="Sources",
        bg="#222222",
        fg="#FFFFFF",
        bd=0,
        highlightthickness=0,
        command=lambda: button_click(sources_btn),
        relief="flat",
        cursor="hand2"
    )
    sources_btn.place(
        x=12.0,
        y=14.0,
        width=151.0,
        height=36.0
    )

    feed_btn = Button(
        window,
        text="Feed",
        bg="#222222",
        fg="#FFFFFF",
        bd=0,
        highlightthickness=0,
        command=lambda: button_click(feed_btn),
        relief="flat",
        cursor="hand2"
    )
    feed_btn.place(
        x=12.0,
        y=75.0,
        width=151.0,
        height=36.0
    )

    queue_btn = Button(
        window,
        text="Queue",
        bg="#222222",
        fg="#FFFFFF",
        bd=0,
        highlightthickness=0,
        command=lambda: button_click(queue_btn),
        relief="flat",
        cursor="hand2"
    )
    queue_btn.place(
        x=12.0,
        y=136.0,
        width=151.0,
        height=36.0
    )

    buttons = [sources_btn, feed_btn, queue_btn]

    exit_btn = Button(
        window,
        text="Exit",
        bg="#222222",
        fg="#FFFFFF",
        bd=0,
        highlightthickness=0,
        command=lambda: window.destroy(),
        relief="flat",
        cursor="hand2"
    )
    exit_btn.place(
        x=12.0,
        y=623.0,
        width=151.0,
        height=36.0
    )

    ############################################################################################################
    # Sources section
    sources_frame = tk.Canvas(window, bg="#d9d9d9", width=1050, height=644, highlightthickness=0, bd=0)
    sources_frame.place(x=1239.0, y=659.0)


    ##############################################################################################################################
    # Feed section
    feed_frame = tk.Canvas(window, bg="#d9d9d9", width=1050, height=644, highlightthickness=0, bd=0)
    feed_frame.place(x=1239.0, y=659.0)


    ##############################################################################################################################
    # Create the queue_frame
    queue_frame = tk.Frame(window, bg="#d9d9d9", width=1253, height=644, highlightthickness=0, bd=0)
    queue_frame.place(x=1239.0, y=659.0)

    
    ##############################################################################################################################
    def button_click(button):
        # Change background color of all buttons to initial color
        for btn in buttons:
            btn.config(bg="#222222")
        # Change background color of the clicked button to a little brighter
        button.config(bg="#444")

        if button == sources_btn:
            load_sources_frame(sources_frame, feed_btn)
        
            sources_frame.place_configure(x=186.0, y=14.0)
            feed_frame.place_configure(x=1000.0, y=1000.0)
            queue_frame.place_configure(x=1000.0, y=1000.0)

        elif button == feed_btn:
            load_feed_frame(feed_frame, feed_btn)
        
            feed_frame.place_configure(x=186.0, y=14.0)
            sources_frame.place_configure(x=1000.0, y=1000.0)
            queue_frame.place_configure(x=1000.0, y=1000.0)
        
        elif button == queue_btn:
            load_queue_frame(queue_frame, queue_btn)
        
            feed_frame.place_configure(x=1000.0, y=1000.0)
            sources_frame.place_configure(x=1000.0, y=1000.0)
            queue_frame.place_configure(x=186.0, y=14.0)

    window.resizable(False, False)
    # Automatically click the "Sources" button
    sources_btn.invoke()

    window.mainloop()

load_main_window()