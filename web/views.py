from django.shortcuts import render
from django.http import JsonResponse

import json, os, pprint
from application_only_auth import Client


CONSUMER_KEY = os.environ["CONSUMER_KEY"]
CONSUMER_SECRET = os.environ["CONSUMER_SECRET"]
client = Client(CONSUMER_KEY, CONSUMER_SECRET)

def index(request):
    return render(request, 'web/index.html', {})

def get_user(request):
    user = client.request('https://api.twitter.com/1.1/users/show.json?screen_name=barackobama')

    # Delete later
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(user)

    # Preprocess image to get larger resolution
    normal_index = user["profile_image_url"].find("normal.png")
    profile_large = user["profile_image_url"][:normal_index]
    print profile_large
    data = {
        "photo_link": user["profile_image_url_https"],
        "name": "Bob",
        "handle": "bob",
        "description": "welcome to my twitter page",
        "location": "santa monica",
        "external_link": "www.mypace.com",
        "join_date": "Feb 2, 1992",
        "tweetscore": 740,
        "follower_count": 33,
        "tweet_content": 0.8,
        "followers_score": 0.3,
        "tweets": [
            {
            "retweet_count": 3,
            "media": "http://thelistenersclub.timothyjuddviolin.com/wp-content/uploads/sites/2/2014/08/small_waves_1920x1200.jpg",
            "text": "My fake tweet"
            }
        ]
    }
    return JsonResponse({'hello': 'world'})

def get_tweets(request):
    pass

def get_friends(request):
    pass

def get_users(request):
    pass
