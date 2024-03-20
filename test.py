from requests_oauthlib import OAuth1Session
import os

# Replace placeholders with your API data
consumer_key = "yWT3VnblbzVscfjK8bLVZSvyO"
consumer_secret = "WLOXuk0mJQ344jEGCuXBY58w3birslhYgy8VgProeYwzZWuFPo"
access_token = "1762926841638117376-Zi3vPML6wSrBk9U7cUMguSJitrQMxP"
access_token_secret = "ybGhBalhgvD2Owt5wRGnBmUY3H6tfHHQri9Lb1fWguFf4"

# OAuth1 session initialization
oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)

# Step 1: Obtain request token
request_token_url = "https://api.twitter.com/oauth/request_token"
fetch_response = oauth.fetch_request_token(request_token_url)
resource_owner_key = fetch_response.get("oauth_token")
resource_owner_secret = fetch_response.get("oauth_token_secret")
print("Got OAuth token: %s" % resource_owner_key)

# Step 2: Obtain authorization
base_authorization_url = "https://api.twitter.com/oauth/authorize"
authorization_url = oauth.authorization_url(base_authorization_url)
print("Please go here and authorize: %s" % authorization_url)
verifier = input("Paste the PIN here: ")

# Step 3: Obtain access token
access_token_url = "https://api.twitter.com/oauth/access_token"
oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=resource_owner_key,
    resource_owner_secret=resource_owner_secret,
    verifier=verifier,
)
oauth_tokens = oauth.fetch_access_token(access_token_url)

access_token = oauth_tokens["oauth_token"]
access_token_secret = oauth_tokens["oauth_token_secret"]

# OAuth1 session initialization with access token
oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=access_token,
    resource_owner_secret=access_token_secret,
)

# Make the request to post a tweet
tweet_text = "Hello world!"
response = oauth.post("https://api.twitter.com/2/tweets", json={"text": tweet_text})

# Check response
if response.status_code != 201:
    raise Exception("Request returned an error: {} {}".format(response.status_code, response.text))

print("Response code: {}".format(response.status_code))
print("Tweet posted successfully!")
