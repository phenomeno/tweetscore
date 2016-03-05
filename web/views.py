from django.shortcuts import render

def index(request):
    data = {
        "photo_link": "http://thelistenersclub.timothyjuddviolin.com/wp-content/uploads/sites/2/2014/08/small_waves_1920x1200.jpg",
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
    return render(request, 'web/index.html', {"data": data})
