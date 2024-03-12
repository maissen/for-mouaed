import pickle
from tkinter import Tk, Canvas, Entry, Button, Text, Scrollbar, Frame, Label
from tkinter.ttk import Combobox
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import feedparser
import os
import webbrowser
import requests
from io import BytesIO
import os
from datetime import datetime        
import re
import tweepy

def open_txt_file(file_name):
    try:
        current_dir = os.path.dirname(os.path.realpath(__file__))
        # Construct the file path for sample.txt
        file_path = os.path.join(current_dir, file_name)
        os.startfile(file_path)
    except:
        popup_message('Error', f'{file_name} file is not found!\nplease create a new one with necessary data.')


def delete_post_from_queue(post, queue_btn):
    try:
        with open('queue_list.dat', 'rb') as file:
            queue_list = pickle.load(file)
            queue_list_filtered = [item for item in queue_list if item['title'] != post['title']]
        with open('queue_list.dat', 'wb') as file:
            pickle.dump(queue_list_filtered, file)
    except FileNotFoundError:
        # print("File 'queue_list.dat' not found. Creating a new file with an empty list.")
        queue_list = []
        with open('queue_list.dat', 'wb') as file:
            pickle.dump(queue_list, file)
    queue_btn.invoke()


def verify_post(hashtags, title, description):
    return (len(hashtags) + len(title) + len(description)) < 280


def add_to_queue(entry, hashtags, title, description, img_is_included, entry_img_url):
    try:
        if os.path.exists('queue_list.dat') and os.path.getsize('queue_list.dat') > 0:
            with open('queue_list.dat', 'rb') as file:
                queue_list = pickle.load(file)
        else:
            queue_list = []
        
        if(verify_post(hashtags, title, description)):
            if img_is_included:
                queue_list.insert(0, {"entry": entry,"title": title, "description": description, "hashtags": hashtags, 'img_is_included': img_is_included, 'entry_img_url': entry_img_url})
            else:
                queue_list.insert(0, {"entry": entry,"title": title, "description": description, "hashtags": hashtags, 'img_is_included': img_is_included, 'entry_img_url': ''})
        else:
            popup_message('Error', 'Your post length shouldn\'t exceed 280 text length!')

        with open('queue_list.dat', 'wb') as file:
            pickle.dump(queue_list, file)
            # print('Entry is uploaded successfully!')
    except FileNotFoundError:
        # print("File 'queue_list.dat' not found. Creating a new file with an empty list.")
        queue_list = []
        with open('queue_list.dat', 'wb') as file:
            pickle.dump(queue_list, file)


def get_entry_picture(entry):
    picture_url = None
    if 'media_content' in entry:
        picture_url = entry.media_content[0]['url']
    elif 'enclosures' in entry and entry.enclosures:
        picture_url = entry.enclosures[0]['url']
    return picture_url


def update_variables(x, parsed_title, number_of_parsed_entries):
    data = {
        'x': x,
        'parsed_title': parsed_title,
        'number_of_parsed_entries': number_of_parsed_entries
    }
    with open("variables.dat", "wb") as file:
        pickle.dump(data, file)


def delete_variables():
    with open("variables.dat", "wb") as file:
        file.write(b'')  # Write an empty byte string to clear the contents


def create_variables():
    data = {'x': {}, 'parsed_title': '', 'number_of_parsed_entries': 0}
    try:
        with open("variables.dat", "wb") as file:
            pickle.dump(data, file)
    except FileNotFoundError:
        with open("variables.dat", "wb") as file:
            pickle.dump(data, file)


def load_variables():
    with open("variables.dat", "rb") as file:
        data = pickle.load(file)
    return data


def load_hashtags_function(entry):
    try:
        all_hashtags = ''
        with open("Hashtags.txt", "r") as file:
            for line in file:
                all_hashtags += line.strip() + " "
                
            entry.delete('1.0', 'end')
            entry.insert("1.0", f"{all_hashtags}")
        return all_hashtags
    except FileNotFoundError:
        with open("Hashtags.txt", "w") as file:
            return ""


def load_saved_sources(saved_links_input):
    try:
        with open("My_rss_sources.dat", "rb") as file:
            rss_sources = pickle.load(file)
            titles = [source["title"] for source in rss_sources]
            if titles:
                saved_links_input["values"] = titles
                saved_links_input.set(titles[0])
    except FileNotFoundError:
        with open("My_rss_sources.dat", "wb") as file:
            rss_sources = []
            pickle.dump(rss_sources, file)


def destroy_frame_child_elements(frame):
    # Get the list of all child widgets of the frame
    children = frame.winfo_children()

    # Destroy each child widget
    for child in children:
        child.destroy()


def popup_message(title, message):
    # Create the popup window
    popup = tk.Toplevel()
    popup.title(title)
    popup_width = 350
    popup_height = 80

    # Hide the title bar
    popup.overrideredirect(True)

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


def share_post(post_data):
    try:
        with open("api.txt", "r") as file:
            content = file.read()
    except FileNotFoundError:
        popup_message("Error", "Please check your 'api.txt' file!")
    else:
        pattern = r'"(.*?)"' # Define a pattern to match the values between the quotes
        matches = re.findall(pattern, content) # Use regex to find all matches
        api_key = matches[0]
        api_key_secret = matches[1]
        bearer_token = matches[2]
        client_id = matches[3]
        client_secret = matches[4]
        access_token = matches[5]
        access_token_secret = matches[6]

        try:
            client = tweepy.Client(bearer_token, api_key, api_key_secret, access_token, access_token_secret)
            auth = tweepy.OAuth1UserHandler(api_key, api_key_secret, access_token, access_token_secret)
            api = tweepy.API(auth)

            hashtags = post_data['hashtags'].split()
            formatted_hashtags = []
            for hashtag in hashtags:
                formatted_hashtags.append("#" + hashtag + "\n")
            formatted_hashtags_str = " ".join(formatted_hashtags)

            pub_date_datetime = datetime.strptime(post_data['entry']['published'], "%a, %d %b %Y %H:%M:%S %z")
            pub_date_formatted = f"{pub_date_datetime.strftime("%d %b %Y")}"

            if post_data['img_is_included']:
                picture_url = post_data['entry_img_url']
                post = f"{post_data['title']}\n\n{post_data['description']}\nShared on : {pub_date_formatted}\n{formatted_hashtags_str}\n\n{picture_url}"
                client.create_tweet(text=post)
            else:
                post = f"{post_data['title']}\n\n{post_data['description']}\nShared on : {pub_date_formatted}\n{formatted_hashtags_str}"
                client.create_tweet(text=post)

                
        except Exception as e:
            print("Error:", e)
            popup_message('Error', "Oops! an error occurred while sharing your post to Twitter!")
        else:
            popup_message('Success', "Post shared to Twitter successfully!")


def push_posts(queue_data):
    for i in range(len(queue_data)):
        share_post(queue_data[i])
        print(f"Post num {i} is shared successfully!")


def save_rss(saved_links_from_file, rss_title, rss_link):
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

        if "-- There's no RSS saved --" in saved_links_from_file["values"]:
            saved_links_from_file.delete(saved_links_from_file["values"].index("-- There's no RSS saved --"))

        saved_links_from_file["values"] = [source["title"] for source in rss_sources]
        saved_links_from_file.set(title)

        rss_title.delete(0, tk.END)
        rss_link.delete(0, tk.END)

        popup_message("Success", f"{title} saved successfully")
    else:
        if not link:
            popup_message("Error", "Please enter a Link!")
        elif not title:
            popup_message("Error", "Please enter a Title!")


def delete_rss(saved_links_from_file):
    title_to_delete = saved_links_from_file.get()
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
            saved_links_from_file["values"] = [source["title"] for source in updated_sources]
            saved_links_from_file.set(updated_sources[0]["title"])
            popup_message("Success", f"{title_to_delete} deleted successfully")
        else:
            saved_links_from_file["values"] = []
            saved_links_from_file.set("-- There's no RSS saved --")
            popup_message("Warning", "There's no saved RSS to delete")
    else:
        popup_message("Error", "No RSS title selected!")


def delete_confirm_window(saved_links_from_file, rss_source):
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
        delete_rss(saved_links_from_file)
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

    def update_rss(saved_links_from_file, new_title, new_link, window):
        # Check if new_title and new_link are not empty
        if not new_title.strip() or not new_link.strip():
            popup_message("Error", "Please enter both title and link!")
            return

        title_to_update = saved_links_from_file.get()
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
            saved_links_from_file["values"] = [source["title"] for source in rss_sources]
            saved_links_from_file.set(new_title)
            window.destroy()
        else:
            popup_message("Error", "No RSS title selected!")


def update_rss(saved_links_from_file, new_title, new_link, window):
    # Check if new_title and new_link are not empty
    if not new_title.strip() or not new_link.strip():
        popup_message("Error", "Please enter both title and link!")
        return

    title_to_update = saved_links_from_file.get()
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
        saved_links_from_file["values"] = [source["title"] for source in rss_sources]
        saved_links_from_file.set(new_title)
        window.destroy()
    else:
        popup_message("Error", "No RSS title selected!")


def update_rss_window(saved_links_from_file):
    title_to_update = saved_links_from_file.get()
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
                update_button = ttk.Button(window, text="Update", command=lambda: update_rss(saved_links_from_file, title_input.get(), link_input.get(), window))
                update_button.pack(pady=0)

                # Run the main event loop
                window.mainloop()
                
                return  # Exit the function after creating and running the window

        # If the loop completes without finding a matching title, show an error message
        popup_message("Error", "RSS title not found!")
    else:
        popup_message("Error", "No RSS title selected!")


def parse_rss(saved_links_from_file, feed_btn):
    selected_title = saved_links_from_file.get()
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
                    number_of_parsed_entries = len(x.entries)
                    if(number_of_parsed_entries > 0):
                        update_variables(x=x, parsed_title=selected_title, number_of_parsed_entries=number_of_parsed_entries)
                        feed_btn.invoke()
                        
                    else:
                        popup_message("Error", f"No entries from {selected_title}, you can try later!")
                except:
                    popup_message("Error", "Invalid rss link! Please verify the link.")
    

def load_sources_frame(sources_frame, feed_btn):
    destroy_frame_child_elements(sources_frame)

    # Add elements to the parent sources_frame
    sources_frame.create_text(
        492.0 - 186.0,
        129.0 - 14.0,
        anchor="nw",
        text="Enter rss Link :",
        fill="#000000",
        font=("Inter", 15)
    )

    sources_frame.create_text(
        492.0 - 186.0,
        237.0 - 14.0,
        anchor="nw",
        text="Enter rss Title :",
        fill="#000000",
        font=("Inter", 15)
    )

    rss_link = tk.Entry(
        sources_frame,
        bd=0,
        bg="#BEBEBE",
        fg="#000716",
        highlightthickness=0
    )
    rss_link.place(
        x=492.0 - 186.0,
        y=157.0 - 14.0,
        width=439.0,
        height=33.0
    )

    rss_title = tk.Entry(
        sources_frame,
        bd=0,
        bg="#BEBEBE",
        fg="#000716",
        highlightthickness=0
    )
    rss_title.place(
        x=492.0 - 186.0,
        y=265.0 - 14.0,
        width=439.0,
        height=33.0
    )

    sources_frame.create_text(
        623.0 - 186.0,
        46.0 - 14.0,
        anchor="nw",
        text="Add new source",
        fill="#000000",
        font=("Inter", 24)
    )

    saved_links_from_file = Combobox(
        sources_frame,
        state="readonly"
    )
    saved_links_from_file.set("-- There's no RSS saved --")
    saved_links_from_file.place(
        x=492.0 - 186.0,
        y=430.0 - 14.0,
        width=446.0,
        height=39.0
    )
    load_saved_sources(saved_links_from_file)

    delete_btn = tk.Button(
        sources_frame,
        text="Delete",
        bg="#222222",
        fg="#FFFFFF",
        bd=0,
        highlightthickness=0,
        command=lambda: delete_confirm_window(saved_links_from_file, saved_links_from_file.get()),
        relief="flat",
        cursor="hand2"
    )
    delete_btn.place(
        x=808.0 - 186.0,
        y=507.0 - 14.0,
        width=130.0,
        height=36.0
    )

    update_btn = tk.Button(
        sources_frame,
        text="Update",
        bg="#222222",
        fg="#FFFFFF",
        bd=0,
        highlightthickness=0,
         command=lambda: update_rss_window(saved_links_from_file),
        relief="flat",
        cursor="hand2"
    )
    update_btn.place(
        x=650.0 - 186.0,
        y=507.0 - 14.0,
        width=130.0,
        height=36.0
    )

    parse_btn = tk.Button(
        sources_frame,
        text="Parse",
        bg="#222222",
        fg="#FFFFFF",
        bd=0,
        highlightthickness=0,
        command=lambda: parse_rss(saved_links_from_file, feed_btn),
        relief="flat",
        cursor="hand2"
    )
    parse_btn.place(
        x=492.0 - 186.0,
        y=507.0 - 14.0,
        width=130.0,
        height=36.0
    )

    sources_frame.create_text(
        492.0 - 186.0,
        404.0 - 14.0,
        anchor="nw",
        text="Saved Sources",
        fill="#000000",
        font=("Inter", 15)
    )

    sources_frame.create_rectangle(
        561.0 - 186.0,
        92.0 - 14.0,
        861.0016784667969 - 186.0,
        93.0 - 14.0,
        fill="#000000",
        outline=""
    )

    

    add_source = tk.Button(
        sources_frame,
        text="Add Source",
        bg="#222222",
        fg="#FFFFFF",
        bd=0,
        highlightthickness=0,
        relief="flat",
        cursor="hand2",
        command=lambda: save_rss(saved_links_from_file, rss_title, rss_link),
    )
    add_source.place(
        x=622,
        y=305,
        width=130.0,
        height=36.0
    )


# def load_queue_frame(queue_frame, queue_btn):
#     try:
#         # Check if the file exists and is not empty
#         if os.path.exists('queue_list.dat') and os.path.getsize('queue_list.dat') > 0:
#             with open('queue_list.dat', 'rb') as file:
#                 queue_data = pickle.load(file)
#                 # print('queue_list.dat is loaded successfully!')
#         else:
#             # print("File 'queue_list.dat' is empty. Initializing queue_list as an empty list.")
#             queue_data = []
#     except FileNotFoundError:
#         # print("File 'queue_list.dat' not found. Creating a new file with an empty list.")
#         queue_data = []
#         with open('queue_list.dat', 'wb') as file:
#             pickle.dump(queue_data, file)

#     queue_data_length = len(queue_data)

#     destroy_frame_child_elements(queue_frame)
#     # Add text label above the queue_list canvas
#     queue_label = tk.Label(queue_frame, text="Your Queue list", bg="#d9d9d9", fg="black", font=("Inter", 16))
#     queue_label.pack(pady=10)  # Adjust padding according to your preference

#     # Create a canvas to contain the posts
#     queue_canvas = tk.Canvas(queue_frame, bg="#d9d9d9", width=1023, height=543)
#     queue_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # Adjust this according to your layout requirements

#     # Calculate total content height
#     total_content_height = (queue_data_length * (15 + 130)) + 100  # Height of 10 rectangles

#     # Configure canvas scrolling
#     queue_canvas.config(scrollregion=(0, 0, 1010, total_content_height))  # Adjust width according to your content

#     # Create a vertical scrollbar for the canvas
#     scrollbar = tk.Scrollbar(queue_frame, orient="vertical", command=queue_canvas.yview)
#     scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

#     # Configure canvas scrolling
#     queue_canvas.config(yscrollcommand=scrollbar.set)

#     # Create rectangles as posts
#     y = 15
#     for i in range(len(queue_data)):  # Loop only until the second-to-last rectangle
#         post = tk.Canvas(queue_canvas, bg="#d9d9d9", width=996, height=130, highlightbackground="#d9d9d9")
#         queue_canvas.create_window(14, y, anchor="nw", window=post)

#         # Assuming queue_data is a list of dictionaries containing post data
#         title = queue_data[i].get('title', '')
#         description = queue_data[i].get('description', '')
#         hashtags = queue_data[i].get('hashtags', '')

#         # Create Post's title
#         label = tk.Label(post, text="Post title", bg=post.cget('bg'))
#         if len(title) > 250:
#             label = tk.Label(post, text=f"{title[:250]}...", bg=post.cget('bg'))
#         else:
#             label = tk.Label(post, text=f"{title}", bg=post.cget('bg'))
#         label.place(x=180+15, y=10)

#         # Create Posts's description
#         if(description):
#             if len(description) > 350:
#                 label = tk.Label(post, text=f"{description[:350]}...", bg=post.cget('bg'), wraplength=680, anchor="w", justify="left", fg="#484848")
#             else:
#                 label = tk.Label(post, text=f"{description}", bg=post.cget('bg'), wraplength=680, anchor="w", justify="left", fg="#484848")
#         else:
#             label = tk.Label(post, text=f"{"This post doesn't have a description to show!"}", bg=post.cget('bg'), wraplength=680, anchor="w", justify="left", fg="#484848")
#         label.place(x=180+15, y=35)

#         # label of Post's date
#         # Parse the pub_date string into a datetime object
#         pub_date_datetime = datetime.strptime(queue_data[i].get('entry', '').get('published', 'Failed to get entry\'s date'), "%a, %d %b %Y %H:%M:%S %z")
#         hashtags = queue_data[i]['hashtags'].split()
#         formatted_hashtags = []
#         for hashtag in hashtags:
#             formatted_hashtags.append("#" + hashtag + " ")
#         formatted_hashtags_str = " ".join(formatted_hashtags)
#         # Format the datetime object to show only date, month, and year
#         pub_date_formatted = f"{pub_date_datetime.strftime("%d %b %Y")}"
#         label = tk.Label(post, text=pub_date_formatted, bg=post.cget('bg'))
#         label.place(x=180+15, y=102)
#         label = tk.Label(post, text=f"{formatted_hashtags_str}", bg=post.cget('bg'), fg='#2320BF')
#         label.place(x=180+90, y=102)

#         delete_post_from_queue_btn = tk.Button(
#             post,
#             text="D",
#             bg="#222222",
#             fg="#FFFFFF",
#             bd=0,
#             highlightthickness=0,
#             command=lambda: delete_post_from_queue(queue_data[i], queue_btn),
#             relief="flat",
#             cursor="hand2"
#         )
#         delete_post_from_queue_btn.place(
#             x=992-25-3,
#             y=9,
#             width=25,
#             height=25
#         )

#         share_post_from_queue = tk.Button(
#             post,
#             text="P",
#             bg="#222222",
#             fg="#FFFFFF",
#             bd=0,
#             highlightthickness=0,
#             command=lambda: share_post(queue_data[i]),
#             relief="flat",
#             cursor="hand2"
#         )
#         share_post_from_queue.place(
#             x=992-25*2-10,
#             y=9,
#             width=25,
#             height=25
#         )

        
#         ################
#         # To set the entry's img
#         # Create the canvas
#         entry_img_container = Canvas(post, bg="#d7d9e5", width=180, height=130, highlightbackground="#d9d9d9")  # Set desired width and height
#         entry_img_container.place(x=0, y=0)  # Set desired position
#         if queue_data[i]['img_is_included']:
#             entry_img_url = queue_data[i]['entry_img_url']
#             print('img is included')
#             # Load the image from the URL
#             response = requests.get(entry_img_url)
#             image_data = response.content
#             image = Image.open(BytesIO(image_data))

#             # Resize the image to fit the canvas dimensions while maintaining aspect ratio
#             width, height = image.size
#             canvas_width = 180
#             canvas_height = 130
#             aspect_ratio = min(canvas_width / width, canvas_height / height)
#             new_width = int(width * aspect_ratio)
#             new_height = int(height * aspect_ratio)
#             image = image.resize((new_width, new_height))  # Remove Image.ANTIALIAS here

#             # Convert the Image object to a Tkinter PhotoImage
#             photo = ImageTk.PhotoImage(image)

#             # Create an image container on the canvas
#             image_container = entry_img_container.create_image(
#                 canvas_width / 2, canvas_height / 2,
#                 image=photo,
#                 anchor="center"  # Center the image
#             )

#             # Make sure to keep a reference to the photo object to prevent it from being garbage collected
#             entry_img_container.photo = photo
#         else:
#             print('img is not included')
#             # print('This entry doesn\'t have a picture!')
#             # Load a placeholder image from the local file
#             placeholder_image = Image.open("404.jpg")
#             # Get the dimensions of the placeholder image
#             width, height = placeholder_image.size
#             # Calculate the scaling factor to fit the image within the canvas while maintaining aspect ratio
#             scale_factor = min(379 / width, 172 / height)
#             # Resize the placeholder image
#             resized_image = placeholder_image.resize((int(width * scale_factor), int(height * scale_factor)))
#             # Convert the resized Image object to a Tkinter PhotoImage
#             placeholder_photo = ImageTk.PhotoImage(resized_image)
#             # Calculate the x-coordinate to center the image horizontally
#             x_centered = (180 - resized_image.width) // 2
#             # Create an image container on the canvas
#             image_container = entry_img_container.create_image(
#                 x_centered, 0,
#                 image=placeholder_photo,
#                 anchor="nw"  # Set anchor to the top-left corner
#             )
#             # Make sure to keep a reference to the photo object to prevent it from being garbage collected
#             entry_img_container.photo = placeholder_photo

#         ###################

#         y += 15 + 130  # Increment y-coordinate to properly position each child canvas

#     if queue_data_length > 0:
#         push_posts_button = tk.Button(
#             queue_frame,
#             text="Push All Posts",
#             bg="#222222",
#             fg="#FFFFFF",
#             bd=0,
#             highlightthickness=0,
#             command=lambda: push_posts(queue_data),
#             relief="flat",
#             cursor="hand2"
#         )
#         push_posts_button.place(
#             x=425,  # Adjust the x-coordinate to move the button to a visible location
#             y=550,  # Adjust the y-coordinate to move the button to a visible location
#             width=182.0,
#             height=46.0
#         )


def load_feed_frame(feed_frame, feed_btn):
    destroy_frame_child_elements(feed_frame)
    variables = load_variables()
    x = variables["x"]
    parsed_title = variables['parsed_title']
    number_of_parsed_entries = variables['number_of_parsed_entries']

    feed_frame.create_rectangle( #hashtags
    657,
    437,
    1036,
    538.0,
    fill="#9597a8",
    outline="")

    load_hashtags_btn = tk.Button(
        feed_frame,
        text="L",
        bg="#222222",
        fg="#FFFFFF",
        bd=0,
        highlightthickness=0,
        command=lambda: load_hashtags_function(hashtags_entry),
        relief="flat",
        cursor="hand2"
    )
    load_hashtags_btn.place(
        x=997,
        y=443,
        width=30,
        height=30.0
    )

    feed_frame.create_rectangle( #summary
    657,
    324,
    1036,
    425,
    fill="#9597a8",
    outline="")

    feed_frame.create_rectangle( #title
    657,
    209,
    1036,
    310,
    fill="#9597a8",
    outline="")

    entry_title = tk.Text(#title input
        feed_frame,
        bd=0,
        bg="#9597a8",
        fg="#000",
        highlightthickness=0
    )
    entry_title.place(
        x=671,
        y=236,
        width=356,
        height=69
    )
    scrollbar_entry_title = Scrollbar(feed_frame, orient="vertical", width=13, troughcolor="#9597A8", bd=0, command=entry_title.yview)
    entry_title.config(yscrollcommand=scrollbar_entry_title.set)
    scrollbar_entry_title.place(x=1036.0, y=209.0, height=101.0, anchor="nw")

    entry_description = tk.Text( #summary input
        feed_frame,
        bd=0,
        bg="#9597a8",
        fg="#000",
        highlightthickness=0
    )
    entry_description.place(
        x=671,
        y=352,
        width=356,
        height=69
    )
    scrollbar_entry_description = Scrollbar(feed_frame, orient="vertical", width=13, troughcolor="#9597A8", bd=0, command=entry_description.yview)
    entry_description.config(yscrollcommand=scrollbar_entry_description.set)
    scrollbar_entry_description.place(x=1036.0, y=324.0, height=101.0, anchor="nw")

    hashtags_entry = tk.Text( #hashtags input
        feed_frame,
        bd=0,
        bg="#9597a8",
        fg="#000",
        highlightthickness=0
    )
    hashtags_entry.place(
        x=671,
        y=480,
        width=356,
        height=51
    )
    scrollbar_hashtags_entry = Scrollbar(feed_frame, orient="vertical", width=13, troughcolor="#9597A8", bd=0, command=hashtags_entry.yview)
    hashtags_entry.config(yscrollcommand=scrollbar_hashtags_entry.set)
    scrollbar_hashtags_entry.place(x=1036.0, y=437.0, height=101.0, anchor="nw")


    feed_frame.create_text(
    671,
    213.0,
    anchor="nw",
    text="Entry’s Title :",
    fill="#000000",
    font=("Inter", 15 * -1)
    )

    feed_frame.create_text(
        671,
        329,
        anchor="nw",
        text="Entry’s Summary :",
        fill="#000000",
        font=("Inter", 15 * -1)
    )

    feed_frame.create_text(
        671,
        449,
        anchor="nw",
        text="Recent Hashtags :",
        fill="#000000",
        font=("Inter", 15 * -1)
    )

    if parsed_title:
        if (number_of_parsed_entries!=1):
            label = f"From : {parsed_title} ({number_of_parsed_entries} entries)"    
        else:
            label = f"From : {parsed_title} ({number_of_parsed_entries} entry)"

        feed_frame.create_rectangle(
            0,
            0,
            500,
            65,
            fill="#d9d9d9",
            outline="",
            tags="background"
        )

        feed_frame.create_text(
            25,
            15,
            anchor="nw",
            text=label,
            fill="#000000",
            font=("Inter", 12 * -1)
        )

        try:
            if x.feed['title'] != None:
                if len(x.feed.title) <= 40:
                    feed_title = x.feed.title
                else:
                    feed_title = x.feed.title[:40]
            else:
                title_label = ttk.Label(left_frame, text=f"", font=("TkDefaultFont", 20))
                feed_title = f"Feed of {parsed_title}"
        except:
            feed_title = ""

        feed_frame.create_text(
            25,
            34,
            anchor="nw",
            text=feed_title,
            fill="#000000",
            font=("Inter", 20 * -1)
        )

    

    feed_frame.create_rectangle( # entry img
    657,
    23.0,
    657 + 379,
    23 + 172,
    fill="#9597a8",
    outline="")


    def on_enter(event):
        event.widget.config(bg="#9597a8")

    # Function to handle mouse leave event
    def on_leave(event):
        event.widget.config(bg="#d9d9d9")

    def on_double_click(event, entry):
        entry_link = entry.link
        entry_title.delete(1.0, "end")
        entry_description.delete(1.0, "end")

        if('title' in entry.keys()):
            entry_title.delete('1.0', 'end')
            if('title_detail' in entry.keys() and entry.title_detail.type == 'text/plain' and entry.title_detail.value != entry.title):
                entry_title.insert('1.0', f"{entry.title}\n\n-- Title-detail: {entry.title_detail.value}")
            else:
                entry_title.insert("1.0", f"{entry.title}")
        else:
            entry_title.insert("1.0", "This entry doesn't have a title to show!")
            
        
        if('summary' in entry.keys()): 
            entry_description.delete('1.0', 'end')
            if('summary_details' in entry.keys() and entry.summary_detail.type == 'text/plain'):
                entry_description.insert("1.0", f"{entry.summary}\n\n-- Summary-detail: {entry.summary_detail.value}")
            else:
                entry_description.insert("1.0", f"{entry.summary}")
        elif ('description' in entry.keys()): 
            entry_description.delete('1.0', 'end')
            if('description_details' in entry.keys() and entry.description_detail.type == 'text/plain'):
                entry_description.insert("1.0", f"{entry.description}\n\n-- Description-detail: {entry.description_detail.value}")
            else:
                entry_description.insert("1.0", f"{entry.description}")
        else:
            entry_description.delete('1.0', 'end')
            entry_description.insert("1.0", "This entry doesn't have a description or summary to show!")


        entry_img_url = get_entry_picture(entry)
        if entry_img_url is not None:
            # print('This entry has a picture!')
            # Create the canvas
            entry_img_container = Canvas(feed_frame, bg="#d7d9e5", width=379, height=172)  # Set desired width and height
            entry_img_container.place(x=657, y=23)  # Set desired position

            checkbox_state = tk.BooleanVar()
            checkbox_state.set(False)  # Set initial value to False

            def show_state():
                print("Checkbox state:", checkbox_state.get())

            # Create the checkbox
            checkbox = tk.Checkbutton(entry_img_container, text="Include picture:", variable=checkbox_state, command=show_state, bg='#d9d9d9')
            checkbox.place(x=5, y=150)
            

            # Load the image from the URL
            response = requests.get(entry_img_url)
            image_data = response.content
            image = Image.open(BytesIO(image_data))

            # Resize the image to fit the canvas dimensions while maintaining aspect ratio
            width, height = image.size
            canvas_width = 379
            canvas_height = 172
            aspect_ratio = min(canvas_width / width, canvas_height / height)
            new_width = int(width * aspect_ratio)
            new_height = int(height * aspect_ratio)
            image = image.resize((new_width, new_height))  # Remove Image.ANTIALIAS here

            # Convert the Image object to a Tkinter PhotoImage
            photo = ImageTk.PhotoImage(image)

            # Create an image container on the canvas
            image_container = entry_img_container.create_image(
                canvas_width / 2, canvas_height / 2,
                image=photo,
                anchor="center"  # Center the image
            )

            # Make sure to keep a reference to the photo object to prevent it from being garbage collected
            entry_img_container.photo = photo
        else:
            img_is_included = False
            # print('This entry doesn\'t have a picture!')
            # Create the canvas
            entry_img_container = Canvas(feed_frame, bg="#d7d9e5", width=379, height=172)  # Set desired width and height
            entry_img_container.place(x=657, y=23)  # Set desired position
            # Load a placeholder image from the local file
            placeholder_image = Image.open("404.jpg")
            # Get the dimensions of the placeholder image
            width, height = placeholder_image.size
            # Calculate the scaling factor to fit the image within the canvas while maintaining aspect ratio
            scale_factor = min(379 / width, 172 / height)
            # Resize the placeholder image
            resized_image = placeholder_image.resize((int(width * scale_factor), int(height * scale_factor)))
            # Convert the resized Image object to a Tkinter PhotoImage
            placeholder_photo = ImageTk.PhotoImage(resized_image)
            # Calculate the x-coordinate to center the image horizontally
            x_centered = (379 - resized_image.width) // 2
            # Create an image container on the canvas
            image_container = entry_img_container.create_image(
                x_centered, 0,
                image=placeholder_photo,
                anchor="nw"  # Set anchor to the top-left corner
            )
            # Make sure to keep a reference to the photo object to prevent it from being garbage collected
            entry_img_container.photo = placeholder_photo




        search_btn = Button(
        feed_frame,
        text="Search",
        bg="#222222",
        fg="#FFFFFF",
        bd=0,
        highlightthickness=0,
        command=lambda: webbrowser.open(entry.link),
        relief="flat",
        cursor="hand2"
        )
        search_btn.place(
            x=657,
            y=575.0,
            width=182.0,
            height=46.0
        )

        add_to_queue_btn = Button(
        feed_frame,
        text="Add to Queue",
        bg="#222222",
        fg="#FFFFFF",
        bd=0,
        highlightthickness=0,
        command=lambda: add_to_queue(entry, hashtags_entry.get("1.0", "end-1c"), entry_title.get("1.0", "end-1c"), entry_description.get("1.0", "end-1c"), checkbox_state.get(), entry_img_url),
        relief="flat",
        cursor="hand2"
        )
        add_to_queue_btn.place(
            x=854,
            y=575.0,
            width=182.0,
            height=46.0
        )



    # Create a canvas
    entries_frame = Canvas(feed_frame, bg="#D7D9E5", height=538, width=590, bd=0, highlightthickness=0, relief="ridge")
    entries_frame.place(x=25, y=69)

    # Add vertical scrollbar
    scrollbar = Scrollbar(feed_frame, orient="vertical")
    scrollbar.place(x=25 + 590 + 10, y=69, height=538)

    # Configure entries_frame scrolling
    entries_frame.config(yscrollcommand=scrollbar.set)

    # Bind scrollbar to entries_frame
    scrollbar.config(command=entries_frame.yview)

    # Create a frame to contain the labels
    entries_list = Frame(entries_frame, bg="", width=590)
    entries_frame.create_window((0, 0), window=entries_list, anchor='nw')

    # loading the entries in the entries list container 
    for i in range(number_of_parsed_entries):
        label = Label(
            entries_list, 
            text=f"{i+1}. {x.entries[i].title}", 
            bg="#d9d9d9", 
            width=90,  
            anchor='w', 
            padx=7, 
            pady=7, 
            cursor='hand2', 
            wraplength=590, 
            justify='left'
        )
        label.pack(pady=0, fill='x')
        label.bind("<Enter>", on_enter)
        label.bind("<Leave>", on_leave)
        label.bind("<Double-1>", lambda event, index=i: on_double_click(event, x.entries[index])) # for double clicks

    # Function to update scroll region
    def update_scroll_region(event):
        entries_frame.configure(scrollregion=entries_frame.bbox("all"))

    # Bind the update_scroll_region function to the frame's size change event
    entries_list.bind("<Configure>", update_scroll_region)





