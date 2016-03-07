from django.http import JsonResponse

import json, os, pprint, redis
from application_only_auth import Client


CONSUMER_KEY = os.environ["CONSUMER_KEY"]
CONSUMER_SECRET = os.environ["CONSUMER_SECRET"]
client = Client(CONSUMER_KEY, CONSUMER_SECRET)

def get_user(request, screen_name):
    user = client.request('https://api.twitter.com/1.1/users/show.json?screen_name='+screen_name)

    # Preprocess image to get larger resolution
    profile_original = ""
    if user.get("profile_image_url"):
        normal_index = user.get("profile_image_url").find("normal.png")
        profile_original = user.get("profile_image_url")[:normal_index-1]+'.png'

    data = {
        "photo_link": profile_original,
        "name": user.get("name"),
        "handle": screen_name,
        "description": user.get("description"),
        "location": user.get("location"),
        "external_link": user.get("entities").get("url").get("urls")[0].get("expanded_url"),
        "join_date": user["created_at"],
        "follower_count": user["friends_count"],
    }

    # Need to add in user score before we send off but for that we need the tweets.. maybe just consolidate into one endpoint?

    return JsonResponse(data)

def get_tweets(request, screen_name):
    # Can request 300 times per 15 min, get 200 tweets per request = 60,000 tweets per 15 min
    # Can only get up to 3,200 of a user's most recent tweets via this endpoint
    # Need to implement 'cursoring'. First call only needs to specify a count (we'll max it out)
    # Keep track of the lowest ID received and send that as max_id. It'll return max id again so subtract one.
    tweets = client.request('https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name='+screen_name+'&count=1')

    # Create mini tweet to send to client and to send to redis cache.
    minified_tweets = []
    for tweet in tweets:
        mini_tweet = {
            "created_at": tweet.get("created_at"),
            "retweet_count": tweet.get("retweet_count"),
            "text": tweet.get("text"),
            "media": tweet.get("entities").get("media")
        }
        minified_tweets.append(mini_tweet)
    return JsonResponse({tweets: minified_tweets})

def get_friends(screen_name):
    # This gets you 5,000 user ids. Use friends.get("next_cursor") to get next page.
    # Need to think about if we really want to inspect more than 5k friends to get score.
    # Should I stringify_ids=True ??
    friends = client.request('https://api.twitter.com/1.1/friends/ids.json?screen_name='+screen_name)

def get_users(user_ids):
    users = client.request('https://api.twitter.com/1.1/users/lookup.json?user_id='+user_ids)
