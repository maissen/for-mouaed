import feedparser
import webbrowser
import time
import pickle

# link = "https://news.microsoft.com/feed/"
# x = feedparser.parse(link)

'''
['title', 'title_detail', 'links', 'link', 'authors', 'author', 'author_detail', 'published', 'published_parsed', 'tags', 'id', 'guidislink', 'summary', 'summary_detail', 'content']
'''

with open('feed.dat', "rb") as file:
    x = pickle.load(file)

# print(x.entries[0])




def check_current_entry_picture():
    feed = feedparser.parse("https://dwh.lequipe.fr/api/edito/rss?path=/Football/")
    if len(feed.entries) > 0:
        current_entry = feed.entries[0]
        if 'media_content' in current_entry:
            picture_url = current_entry.media_content[0]['url']
            print("URL of the picture:", picture_url)
            print(picture_url)
        elif 'enclosures' in current_entry and current_entry.enclosures:
            picture_url = current_entry.enclosures[0]['url']
            print(picture_url)
        else:
            print("Entry doesn't have a picture")
    else:
        print("No entries found in the feed")

# Example usage:
check_current_entry_picture()
