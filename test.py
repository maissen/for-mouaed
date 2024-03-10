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



'''
API Key : rbVv4cZS6laGp4GERZxB5FH3M
API Key Secret : rp3SNfM7YOg8TakpEUTeuGxs3MF5Y3tKut7rCSYBrh4l5b6r1d
Bearer Token : AAAAAAAAAAAAAAAAAAAAAPdPsgEAAAAAWQWGmV7HJXIYNVd7vwPTqfpxIpU%3DHZp7PvAhKUXld1Xh94fosP5SOuNF3qUzBgGNPR7X8tpXsU6VxL
Client ID : Z1FRRHlJRGxMSUJfdkVKdXBra206MTpjaQ
Client Secret : CfRJ0gOywH0fmXrag2izUhtA-wRi0px-ZRAFSTDXORvhgZ3uHV
Access Token : 1762926841638117376-TOR3Q7Mw71rMvJn7tCRC5rYf8d78yy
Access Token Secret : V1ma7CuWddNEbDQD9t6zRB1JmDst4QtWIai3gusRLkkus
'''
import tweepy
api_key = "rbVv4cZS6laGp4GERZxB5FH3M"
api_secret = "rp3SNfM7YOg8TakpEUTeuGxs3MF5Y3tKut7rCSYBrh4l5b6r1d"
bearer_token = "AAAAAAAAAAAAAAAAAAAAAPdPsgEAAAAAWQWGmV7HJXIYNVd7vwPTqfpxIpU%3DHZp7PvAhKUXld1Xh94fosP5SOuNF3qUzBgGNPR7X8tpXsU6VxL"
access_token = "1762926841638117376-TOR3Q7Mw71rMvJn7tCRC5rYf8d78yy"
access_token_secret = "V1ma7CuWddNEbDQD9t6zRB1JmDst4QtWIai3gusRLkkus"

client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)
auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
api = tweepy.API(auth)

# client.create_tweet(text = "Hello Maissen Belgacem ^^")



import re

# Read the content of the text file
try:
    with open("api.txt", "r") as file:
        content = file.read()
except FileNotFoundError:
    print("Error: File 'api.txt' not found.")

# Define a pattern to match the values between the quotes
pattern = r'"(.*?)"'

# Use regex to find all matches
matches = re.findall(pattern, content)

# Assign the matches to variables
api_key = matches[0]
api_key_secret = matches[1]
bearer_token = matches[2]
client_id = matches[3]
client_secret = matches[4]
access_token = matches[5]
access_token_secret = matches[6]
