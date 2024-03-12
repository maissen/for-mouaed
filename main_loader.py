from tkinter import Tk, Canvas
from PIL import Image, ImageTk, ImageSequence
from main_window import load_main_window
import pygame.mixer

# Global variables
global_image = None
frame_idx = 0

def main_loader():
    def on_drag(event):
        x = window.winfo_pointerx() - window._offset_x
        y = window.winfo_pointery() - window._offset_y
        window.geometry(f"+{x}+{y}")

    def start_drag(event):
        window._offset_x = event.x
        window._offset_y = event.y

    def update_frame(canvas, image_item):
        global global_image, frame_idx
        frame_idx += 1
        if frame_idx < len(global_image):
            canvas.itemconfig(image_item, image=global_image[frame_idx])
            window.after(50, update_frame, canvas, image_item)
        else:
            play_notification_sound()
            # Delay for the sound to finish playing before closing the window
            window.after(2000, lambda: window.destroy())

    def play_notification_sound():
        pygame.mixer.init()
        pygame.mixer.music.load("Twitter Notification Sound Effect.mp3")
        pygame.mixer.music.play()

    window = Tk()

    window_width = 800
    window_height = 600

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

    global global_image
    gif_frames = Image.open("loader.gif")
    global_image = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(gif_frames)]

    # Create a canvas to display the image
    canvas = Canvas(window, width=window_width, height=window_height, bg="#FFFFFF", highlightthickness=0)
    image_item = canvas.create_image(window_width // 2, window_height // 2, image=global_image[frame_idx])
    canvas.pack()

    # Bind mouse events for dragging
    canvas.bind("<B1-Motion>", on_drag)
    canvas.bind("<Button-1>", start_drag)

    # Start updating the frames
    update_frame(canvas, image_item)

    window.mainloop()

main_loader()
