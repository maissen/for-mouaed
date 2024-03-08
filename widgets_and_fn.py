import tkinter as tk
from tkinter import ttk
import feedparser
from my_functions import *
import pickle
import webbrowser
            

def parse_rss(saved_links_input):
    selected_title = saved_links_input.get()
    if selected_title:
        try:
            with open("My_rss_sources.dat", "rb") as file:
                rss_sources = pickle.load(file)
        except FileNotFoundError:
            rss_sources = []

        for source in rss_sources:
            if source["title"] == selected_title:
                link = source['link']
                try:
                    x = feedparser.parse(link)
                    if(len(x.entries) > 0):
                        entries_window(x, source["title"])
                    else:
                        popup_message("Error", "link is not valid or you can try later!")
                except:
                    popup_message("Error", "Invalid rss link! Please verify the link.")
                break
        
        

def save_rss(saved_links_input, rss_title, rss_link):
    title = rss_title.get()
    link = rss_link.get()
    
    if title and link:
        try:
            with open("My_rss_sources.dat", "rb") as file:
                rss_sources = pickle.load(file)
        except FileNotFoundError:
            rss_sources = []

        for source in rss_sources:
            if source["title"] == title:
                popup_message("Error", "RSS title already exists!")
                return
            if source["link"] == link:
                popup_message("Error", "RSS link already exists!")
                return

        rss_sources.append({"title": title, "link": link})
        with open("My_rss_sources.dat", "wb") as file:
            pickle.dump(rss_sources, file)

        if "-- There's no RSS saved --" in saved_links_input["values"]:
            saved_links_input.delete(saved_links_input["values"].index("-- There's no RSS saved --"))

        saved_links_input["values"] = [source["title"] for source in rss_sources]
        saved_links_input.set(title)

        rss_title.delete(0, tk.END)
        rss_link.delete(0, tk.END)

        popup_message("Success", f"{title} saved successfully")
    else:
        if not link:
            popup_message("Error", "Please enter a Link!")
        elif not title:
            popup_message("Error", "Please enter a Title!")
            
            

def delete_rss(saved_links_input):
    title_to_delete = saved_links_input.get()
    if title_to_delete:
        try:
            with open("My_rss_sources.dat", "rb") as file:
                rss_sources = pickle.load(file)
        except FileNotFoundError:
            rss_sources = []

        updated_sources = [source for source in rss_sources if source["title"] != title_to_delete]

        with open("My_rss_sources.dat", "wb") as file:
            pickle.dump(updated_sources, file)

        if updated_sources:
            saved_links_input["values"] = [source["title"] for source in updated_sources]
            saved_links_input.set(updated_sources[0]["title"])
            popup_message("Success", f"{title_to_delete} deleted successfully")
        else:
            saved_links_input["values"] = []
            saved_links_input.set("-- There's no RSS saved --")
            popup_message("Warning", "There's no saved RSS to delete")
    else:
        popup_message("Error", "No RSS title selected!")
        

            
def delete_confirm_window(saved_links_input, rss_source):
    # Create the main window
    window = tk.Tk()
    window.title("Delete Confirmation")

    # Set window width and height
    window_width = 400
    window_height = 140

    # Calculate the center position of the screen
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    # Set window geometry
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Create label
    label = ttk.Label(window, text=f"Are you sure you want to delete {rss_source}?")
    label.pack(pady=20)

    # Function to handle delete button click
    def delete_clicked():
        delete_rss(saved_links_input)
        window.destroy()
    
    def cancel_clicked():
        window.destroy()
        

    # Create a frame to hold the buttons aligned to the right
    button_frame = ttk.Frame(window)
    button_frame.pack(side="bottom", pady=20)

    # Create the delete button with padding and aligned to the right
    delete_button = ttk.Button(button_frame, text="Delete", command=delete_clicked)
    delete_button.pack(side="right", padx=10)

    # Create the cancel button with padding and aligned to the right
    cancel_button = ttk.Button(button_frame, text="Cancel", command=cancel_clicked)
    cancel_button.pack(side="right", padx=10)

    # Run the main event loop
    window.mainloop()




def update_rss(saved_links_input, new_title, new_link, window):
    # Check if new_title and new_link are not empty
    if not new_title.strip() or not new_link.strip():
        popup_message("Error", "Please enter both title and link!")
        return

    title_to_update = saved_links_input.get()
    if title_to_update:
        try:
            with open("My_rss_sources.dat", "rb") as file:
                rss_sources = pickle.load(file)
        except FileNotFoundError:
            rss_sources = []

        # Check if the new title or link already exists
        for source in rss_sources:
            if source["title"] != title_to_update:  # Skip the current title being updated
                if source["title"] == new_title:
                    popup_message("Error", "RSS title already exists!")
                    return
                if source["link"] == new_link:
                    popup_message("Error", "RSS link already exists!")
                    return

        # Update the title and link
        for source in rss_sources:
            if source["title"] == title_to_update:
                old_title = source["title"]
                old_link = source["link"]

                source["title"] = new_title
                source["link"] = new_link
                break

        # Save the updated data back to the file
        with open("My_rss_sources.dat", "wb") as file:
            pickle.dump(rss_sources, file)

        # Update the values in the combobox
        saved_links_input["values"] = [source["title"] for source in rss_sources]
        saved_links_input.set(new_title)
        print("Updated!")
        window.destroy()
    else:
        popup_message("Error", "No RSS title selected!")



def update_rss_window(saved_links_input):
    title_to_update = saved_links_input.get()
    if title_to_update:
        try:
            with open("My_rss_sources.dat", "rb") as file:
                rss_sources = pickle.load(file)
        except FileNotFoundError:
            rss_sources = []

        for source in rss_sources:
            if source["title"] == title_to_update:
                old_title = source["title"]
                old_link = source["link"]
                
                # Create main window
                window = tk.Tk()
                window.title("Update RSS")

                # Calculate the center position of the screen
                window_width = 400  # You can adjust this value as needed
                window_height = 200  # You can adjust this value as needed
                screen_width = window.winfo_screenwidth()
                screen_height = window.winfo_screenheight()
                x = (screen_width - window_width) // 2
                y = (screen_height - window_height) // 2

                # Set window geometry
                window.geometry(f"{window_width}x{window_height}+{x}+{y}")

                # Create frame for inputs
                input_frame = ttk.Frame(window)
                input_frame.pack(padx=10, pady=10)

                # Label and input for updating link
                link_label = ttk.Label(input_frame, text="Update link:")
                link_label.grid(row=0, column=0, sticky="w", padx=(0, 5))

                link_input = ttk.Entry(input_frame, width=40)
                link_input.insert(0, old_link)
                link_input.grid(row=0, column=1, sticky="w")

                # Add margin between the two lines
                ttk.Label(input_frame).grid(row=1, columnspan=2, pady=1)

                # Label and input for updating title
                title_label = ttk.Label(input_frame, text="Update title:")
                title_label.grid(row=2, column=0, sticky="w", padx=(0, 5))

                title_input = ttk.Entry(input_frame, width=40)
                title_input.insert(0, old_title)
                title_input.grid(row=2, column=1, sticky="w")

                # Error label
                error_label = ttk.Label(window, text="", foreground="red")
                error_label.pack(pady=(0, 5))

                # Button to update RSS
                update_button = ttk.Button(window, text="Update", command=lambda: update_rss(saved_links_input, title_input.get(), link_input.get(), window))
                update_button.pack(pady=0)

                # Run the main event loop
                window.mainloop()
                
                return  # Exit the function after creating and running the window

        # If the loop completes without finding a matching title, show an error message
        popup_message("Error", "RSS title not found!")
    else:
        popup_message("Error", "No RSS title selected!")

            
            
def popup_message(title, message):
    # Create the popup window
    popup = tk.Toplevel()
    popup.title(title)
    popup_width = 300
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





##
## Main window
def load_main_window():
    # Create main window
    window = tk.Tk()
    window.title("Twitter Bot")
    window.resizable(False, False)  # Make the window unresizable
    
    # Create a frame to contain label and entry for source
    source = ttk.Frame(window)
    source.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
    rss_link_label = ttk.Label(source, text="Enter RSS link for source:") 
    rss_link_label.grid(row=0, column=0, sticky="w", padx=(0, 5))
    rss_link = ttk.Entry(source, width=30)
    rss_link.grid(row=0, column=1, sticky="w", padx=8, pady=10)
    rss_link.configure(background="white")
    
    # Create a frame to contain label and entry for title
    title = ttk.Frame(window)
    title.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")  
    rss_title_label = ttk.Label(title, text="Enter RSS title:") 
    rss_title_label.grid(row=0, column=0, sticky="w", padx=(0, 5))
    rss_title = ttk.Entry(title, width=30) 
    rss_title.grid(row=0, column=1, sticky="w", padx=8, pady=10)
    rss_title.configure(background="white")

    # Create a frame to contain label, entry, and save button for RSS title
    title_save_frame = ttk.Frame(title)
    title_save_frame.grid(row=0, column=2, padx=(10, 0), pady=5, sticky="w")
    save_button = ttk.Button(title_save_frame, text="Save RSS", command=lambda: save_rss(saved_links_input, rss_title, rss_link))
    save_button.grid(row=0, column=0, padx=5)

    # Create a separator
    separator = ttk.Separator(window, orient='horizontal')
    separator.grid(row=2, column=0, sticky='ew', padx=10, pady=5)

    # Create a frame to contain label, combobox, and buttons for saved links
    saved_links = ttk.Frame(window)
    saved_links.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")
    
    saved_links_label = ttk.Label(saved_links, text="Saved Links:") 
    saved_links_label.grid(row=0, column=0, sticky="w", padx=(0, 5))
    
    saved_links_input = ttk.Combobox(saved_links, width=25, state="readonly")
    saved_links_input.grid(row=0, column=1, sticky="w", padx=8, pady=10)
    saved_links_input.configure(background="white")
    saved_links_input.set("-- There's no RSS saved --")

    update_button = ttk.Button(saved_links, text="Update RSS", command=lambda: update_rss_window(saved_links_input))
    update_button.grid(row=0, column=2, padx=5)

    delete_button = ttk.Button(saved_links, text="Delete RSS", command=lambda: delete_confirm_window(saved_links_input, saved_links_input.get()))
    delete_button.grid(row=0, column=3, padx=5)

    parse_button = ttk.Button(saved_links, text="Parse", command=lambda: parse_rss(saved_links_input))
    parse_button.grid(row=0, column=4, padx=5)

    # Load saved RSS sources from file
    load_saved_sources(saved_links_input)

    # Run the main event loop
    window.mainloop()




# Function to be called when "Share now" button is clicked
def push_post_to_twitter(entry_title, entry_summary, hashtags):
    try:
        print("Share Button is clicked!")
        print(f"title : {entry_title}")
        print(f"summary : {entry_summary}")
        print(f"hashtags : {input_hashtags(hashtags)}")
        popup_message("Success", "Post is shared in twitter successfully")
    except:
        popup_message("Error", "Oops, an error occured, please try again!")
    
    
    
################################################################################################################################################################
################################################################################################################################################################
def load_clicked_entry(root, entry, title_entry, summary_entry):
    
    if('title' in entry.keys()):
        if('title_detail' in entry.keys() and entry.title_detail.type == 'text/plain' and entry.title_detail.value != entry.title):
            title_entry.delete('1.0', 'end')  # Delete from the beginning to the end
            title_entry.insert('1.0', f"Title : {entry.title}\n\nTitle-detail: {entry.title_detail.value}")
        else:
            title_entry.delete('1.0', 'end')  # Delete from the beginning to the end
            title_entry.insert("1.0", f"{entry.title}")
    else:
        title_entry.delete('1.0', 'end')  # Delete from the beginning to the end
        title_entry.insert("1.0", "This entry doesn't have a title to show!")
        
    
    if('summary' in entry.keys()): 
        if('summary_details' in entry.keys()):
            summary_entry.delete('1.0', 'end')
            summary_entry.insert("1.0", f"Title : {entry.title}\n\nTitle-detail: {entry.title_detail.value}")
        else:
            summary_entry.delete('1.0', 'end')
            summary_entry.insert("1.0", f"{entry.summary}")
    else:
        summary_entry.delete('1.0', 'end')
        summary_entry.insert("1.0", "This entry doesn't have a summary to show!")
        
    
    
def search_function():
    print("Search button clicked")

def share_function():
    print("Share button clicked")

def load_hashtags_function(root, hashtags_entry):
    try:
        all_hashtags = ''
        with open("Hashtags.txt", "r") as file:
            # Iterate through each line in the file
            for line in file:
                # Print each word in the line (assuming each line contains a single word)
                all_hashtags += line.strip() + " "
                
            hashtags_entry.delete('1.0', 'end')
            hashtags_entry.insert("1.0", f"{all_hashtags}")
    except FileNotFoundError:
        # If the file doesn't exist, create a new one
        print("The file 'Hashtags.txt' doesn't exist. Creating a new file...")
        # Open the file in write mode to create it
        with open("Hashtags.txt", "w") as file:
            print("New file created.")
    
    
    
def entries_window(x, rss_title):
    root = tk.Tk()
    root.title("Two Halves Example")

    # Padding
    padding_x = 15
    padding_y = 15
    bottom_padding = 5  # Adding a little padding at the bottom

    # Get main window width and height
    window_width = 1250 + 2 * padding_x + 20  # Adding 20px to the width
    window_height = 570 + 2 * padding_y + bottom_padding  # Adjusted height to add padding at the bottom

    # Set window size
    root.geometry(f"{window_width}x{window_height}")

    # Calculate the width of each division, considering padding
    division_width = (1250 - padding_x) / 2

    # Calculate the height of each division, considering top and bottom padding
    division_height = 650

    # Adjust y-coordinate for top padding
    top_padding = padding_y // 2

    # Define the margin between the frames
    frame_margin = 20  # Adjust as needed

    # Left side
    left_frame = tk.Frame(root, width=division_width, height=division_height + 250)  # Adjust height here
    left_frame.place(x=padding_x, y=top_padding + padding_y)

    # Right side
    right_frame = tk.Frame(root, width=division_width, height=division_height)
    right_frame.place(x=division_width + 2 * padding_x + frame_margin, y=top_padding + padding_y)  # Adjusted x-coordinate with extra margin

    # Add a frame within the right frame
    custom_frame_height = 150
    custom_frame = tk.Frame(right_frame, width=division_width, height=custom_frame_height, bg="royalblue")
    custom_frame.place(x=0, y=0)

    # Calculate the width of the input frame to occupy 60% of the right frame
    input_frame_width = division_width * 0.6

    # Add a frame under the royalblue frame
    input_frame_height = 150
    input_frame = tk.Frame(right_frame, width=input_frame_width, height=input_frame_height)
    input_frame.place(relx=0.5, rely=1, anchor="s", y=-110)  # Translate the frame 110 pixels above

    # Add labels and text input fields under the input frame
    title_label = tk.Label(input_frame, text="Title:")
    title_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    title_entry = tk.Text(input_frame, height=5, width=50, bg='#ccc')
    title_entry.grid(row=0, column=1, padx=10, pady=10)

    # Adding scrollbar for title entry
    title_scrollbar = tk.Scrollbar(input_frame, orient="vertical", command=title_entry.yview)
    title_scrollbar.grid(row=0, column=2, sticky="ns")
    title_entry.config(yscrollcommand=title_scrollbar.set)

    summary_label = tk.Label(input_frame, text="Summary:")
    summary_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    summary_entry = tk.Text(input_frame, height=5, width=50, bg='#ccc')
    summary_entry.grid(row=1, column=1, padx=10, pady=10)

    # Adding scrollbar for summary entry
    summary_scrollbar = tk.Scrollbar(input_frame, orient="vertical", command=summary_entry.yview)
    summary_scrollbar.grid(row=1, column=2, sticky="ns")
    summary_entry.config(yscrollcommand=summary_scrollbar.set)

    hashtags_label = tk.Label(input_frame, text="Recent Hashtags:")
    hashtags_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
    hashtags_entry = tk.Text(input_frame, height=5, width=50, bg='#ccc')
    hashtags_entry.grid(row=2, column=1, padx=10, pady=10)

    # Adding scrollbar for hashtags entry
    hashtags_scrollbar = tk.Scrollbar(input_frame, orient="vertical", command=hashtags_entry.yview)
    hashtags_scrollbar.grid(row=2, column=2, sticky="ns")
    hashtags_entry.config(yscrollcommand=hashtags_scrollbar.set)

    # Add a frame for the buttons
    buttons_frame = tk.Frame(input_frame)
    buttons_frame.grid(row=3, columnspan=2, padx=10, pady=10, sticky="e")  # Columnspan to cover both columns

    # Add Load Hashtags button
    load_hashtags_button = tk.Button(buttons_frame, text="Load Hashtags", command=lambda: load_hashtags_function(root, hashtags_entry), bg='#ccc', cursor="hand2")
    load_hashtags_button.grid(row=0, column=0, padx=(0, 10))  # Adjust the right padding

    # Add Share button
    share_button = tk.Button(buttons_frame, text="Share", command=lambda: push_post_to_twitter(title_entry.get("1.0", "end-1c"), summary_entry.get("1.0", "end-1c"), hashtags_entry.get("1.0", "end-1c")), bg='#ccc', cursor="hand2")
    share_button.grid(row=0, column=1, padx=(0, 10))  # Adjust the right padding

    # Add Search button
    search_button = tk.Button(buttons_frame, text="Search", command=lambda: webbrowser.open(entry.link), bg='#ccc', cursor="hand2")
    search_button.grid(row=0, column=2)

    # Integrate container_of_entries function contents to the left frame
    # Define the window title
    if "title" in x.feed.keys():
        root.title(x.feed.title)
    else:
        root.title('RSS Feed Entries')

    # Create a label for parsing information
    if len(x.entries) > 1:
        if len(rss_title) <= 30:
            parsing_label = ttk.Label(left_frame, text=f"Parsing from \"{rss_title}\" ( {len(x.entries)} Entries )")
        else:
            parsing_label = ttk.Label(left_frame, text=f"Parsing from \"{rss_title[:30]}\" ( {len(x.entries)} Entries )")
    else:
        parsing_label = ttk.Label(left_frame, text=f"Parsing from \"{rss_title}\" ( {len(x.entries)} Entry )")
    parsing_label.grid(row=0, column=0, padx=10, pady=(5, 0), sticky="nsew")

    # Create a label for the title
    if x.feed.get('title') != None:
        if len(x.feed.title) <= 40:
            title_label = ttk.Label(left_frame, text=f"Feed : {x.feed.title}", font=("TkDefaultFont", 20))
        else:
            title_label = ttk.Label(left_frame, text=f"Feed : {x.feed.title[:40]}...", font=("TkDefaultFont", 20))
    else:
        title_label = ttk.Label(left_frame, text=f"Feed of {rss_title}", font=("TkDefaultFont", 20))
    title_label.grid(row=1, column=0, padx=10, pady=(5, 0), sticky="nsew")

    # Create a separator line
    separator = ttk.Separator(left_frame, orient='horizontal')
    separator.grid(row=2, column=0, sticky='ew', padx=10, pady=(5, 0))

    # Create a frame to contain label and entry for source
    source = ttk.Frame(left_frame)
    source.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")

    # Create a canvas with both vertical and horizontal scrollbars
    canvas = tk.Canvas(left_frame, width=600 + 2 * 15, height=450 + 2 * 15)
    vscrollbar = ttk.Scrollbar(left_frame, orient='vertical', command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    # Configure the canvas and scrollbars
    canvas.configure(yscrollcommand=vscrollbar.set)
    canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
    canvas.grid(row=4, column=0, sticky='nsew')  # Adjusted row to 4
    vscrollbar.grid(row=4, column=1, sticky='ns')  # Adjusted row to 4

    # Add each entry to the frame
    for i, entry in enumerate(x.entries):
        # Create a frame for the entry
        entry_frame = tk.Frame(scrollable_frame, padx=10, pady=9, cursor='hand2', background='SystemButtonFace')
        entry_frame.pack(fill='x', expand=True)

        # Create a label for the entry
        label = tk.Label(
            entry_frame,
            text=f'{i+1}. {entry.title}',
            wraplength=600,
            justify='left',
            cursor='hand2',  # Change cursor to a pointer
            background='SystemButtonFace',
            highlightbackground='lightgray',  # Set the initial background color
            anchor='w'  # Align text to the left
        )
        label.pack(fill='x', expand=True)

        # Bind the double click event to show details of the selected entry
        label.bind('<Double-Button-1>', lambda event, entry=entry: load_clicked_entry(root, entry, title_entry, summary_entry))

        # Bind the Enter event to change the background color on hover
        entry_frame.bind('<Enter>', lambda event, entry_frame=entry_frame: entry_frame.config(background='lightgray'))

        # Bind the Leave event to change the background color back when the cursor leaves
        entry_frame.bind('<Leave>', lambda event, entry_frame=entry_frame: entry_frame.config(background='SystemButtonFace'))

    # Update the canvas to ensure the scrollbar works correctly
    scrollable_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox('all'))

    # Calculate the center position of the screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - root.winfo_reqwidth()) // 2
    y = (screen_height - root.winfo_reqheight()) // 2

    # Set the window position
    root.geometry(f"+{x}+{y}")

    # Configure the grid to resize with the window
    left_frame.grid_rowconfigure(4, weight=1)
    left_frame.grid_columnconfigure(0, weight=1)

    root.mainloop()
    
    
    
    
