import pickle

with open('test.dat', 'wb') as file:
    pickle.dump([0, 1, 2, 3, 4, 5, 6, 7], file)

with open('test.dat', 'rb') as file:
    x = pickle.load(file)
    queue_list = [item for item in x if item != 3]  # Corrected the condition here

with open('test.dat', 'wb') as file:
    pickle.dump(queue_list, file)

with open('test.dat', 'rb') as file:
    x = pickle.load(file)

# print(x)



import tkinter as tk

# Create the main window
def post_viewer():
    window = tk.Tk()
    window.title("Tkinter Window")

    # Set the window dimensions (width x height)
    window.geometry("480x520")
    window.resizable(False, False)

    # Create a canvas for displaying an image
    post_img = tk.Canvas(window, bg="#d9d9d9", width=420, height=200, highlightbackground="#000")
    post_img.place(x=30, y=0)

    # Create a text input field for post content
    post_content = tk.Text(window, height=10, width=52)
    post_content.place(x=30, y=200)

    # Create a text input field for hashtags
    hashtags = tk.Text(window, height=3, width=52)
    hashtags.place(x=30, y=400)

    # Create an exit button
    exit_btn = tk.Button(
        window,
        text="Exit",
        bg="#222222",
        fg="#FFFFFF",
        bd=0,
        highlightthickness=0,
        command=window.destroy,  # Pass the function reference without calling it
        relief="flat",
        cursor="hand2"
    )
    exit_btn.place(
        x=480-65,
        y=490,
        width=50,
        height=25
    )

    save_btn = tk.Button(
        window,
        text="Save",
        bg="#222222",
        fg="#FFFFFF",
        bd=0,
        highlightthickness=0,
        command=window.destroy,  # Pass the function reference without calling it
        relief="flat",
        cursor="hand2"
    )
    save_btn.place(
        x=480-65-50-10,
        y=490,
        width=50,
        height=25
    )
    # Run the Tkinter event loop
    window.mainloop()

post_viewer()



