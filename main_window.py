from tkinter import Tk, Canvas, Entry, Button, Text, Scrollbar, Frame, Label
from tkinter.ttk import Combobox
import tkinter as tk
import pickle
import webbrowser
from my_functions import *
import feedparser
from tkinter import filedialog




def load_main_window():
    create_variables()
    window = Tk()
    window.title("Twitter bot - Maissen Belgacem")
    window.iconbitmap("img/twitter.ico")
    window.iconbitmap("img/twitter.ico")

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
        y=64.0,
        width=151.0,
        height=36.0
    )

    hashtags_btn = Button(
        window,
        text="Hashtags",
        bg="#222222",
        fg="#FFFFFF",
        bd=0,
        highlightthickness=0,
        command=lambda: button_click(hashtags_btn),
        relief="flat",
        cursor="hand2"
    )
    hashtags_btn.place(
        x=12.0,
        y=114,
        width=151.0,
        height=36.0
    )

    api_btn = Button(
        window,
        text="API",
        bg="#222222",
        fg="#FFFFFF",
        bd=0,
        highlightthickness=0,
        command=lambda: button_click(api_btn),
        relief="flat",
        cursor="hand2"
    )
    api_btn.place(
        x=12.0,
        y=164,
        width=151.0,
        height=36.0
    )

    drafts_btn = Button(
        window,
        text="Drafts",
        bg="#222222",
        fg="#FFFFFF",
        bd=0,
        highlightthickness=0,
        command=lambda: button_click(drafts_btn),
        relief="flat",
        cursor="hand2"
    )
    drafts_btn.place(
        x=12.0,
        y=214,
        width=151.0,
        height=36.0
    )

    buttons = [sources_btn, feed_btn, hashtags_btn, api_btn, drafts_btn]

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
    # drafts section
    drafts_frame = tk.Canvas(window, bg="#d9d9d9", width=1050, height=644, highlightthickness=0, bd=0)
    drafts_frame.place(x=1239.0, y=659.0)


    ##############################################################################################################################
    # Create the queue_frame
    # queue_frame = tk.Frame(window, bg="#d9d9d9", width=1253, height=644, highlightthickness=0, bd=0)
    # queue_frame.place(x=1239.0, y=659.0)

    
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
            drafts_frame.place_configure(x=1000.0, y=1000.0)
            # queue_frame.place_configure(x=1000.0, y=1000.0)

        elif button == feed_btn:
            load_feed_frame(feed_frame, feed_btn)
        
            feed_frame.place_configure(x=186.0, y=14.0)
            sources_frame.place_configure(x=1000.0, y=1000.0)
            drafts_frame.place_configure(x=1000.0, y=1000.0)
            # queue_frame.place_configure(x=1000.0, y=1000.0)

        elif button == drafts_btn:
            load_drafts_frame(drafts_frame, drafts_btn)

            drafts_frame.place_configure(x=186.0, y=14.0)
            feed_frame.place_configure(x=1000.0, y=1000.0)
            sources_frame.place_configure(x=1000.0, y=1000.0)
            # queue_frame.place_configure(x=1000.0, y=1000.0)
        
        elif button == hashtags_btn:
            open_txt_file("Hashtags.txt")

        elif button == api_btn:
            open_txt_file("api.txt")

    window.resizable(False, False)
    # Automatically click the "Sources" button
    sources_btn.invoke()

    window.mainloop()

# load_main_window()