from django.http import JsonResponse, HttpResponse
from django.core.cache import cache

import json, os, pprint, re, csv
from application_only_auth import Client


CONSUMER_KEY = os.environ["CONSUMER_KEY"]
CONSUMER_SECRET = os.environ["CONSUMER_SECRET"]
client = Client(CONSUMER_KEY, CONSUMER_SECRET)

temp_data = []
negative_words = []
positive_words = []

def twitter_data(request, screen_name):
    # # Check if user exists in cache
    user = cache.get(screen_name)
    if user is None:
        # FIXME do retweets hold retweeted user object?
        # tweets = client.request('https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name='+screen_name+'&count=2')
        tweets = cache.get("temp_data")
        print "length of tweets list", len(tweets)
        positive_total, negative_total, words_total = 0, 0, 0
        for tweet in tweets:
            score = get_tweet_score(tweet)
            positive_total += score[0]
            negative_total += score[1]
            words_total += score[2]
        print positive_total, negative_total, words_total
        content_score = (positive_total - negative_total) / words_total
        print content_score
        # friends_count = tweets[0].get("user").get("friends_count")
        # friends_ids = get_friends(screen_name)
        # friends_user_objects = get_users(friends_ids)
        # friends_total_score = 0
        # for friend in friends_user_objects:
        #     friend_score = get_friend_score(friend)
        #     friend["friend_score"] = friend_score
        #     cache.set(friend.get("screen_name"), friend, timeout=86400)
        #     friends_total_score += friends_score
        # friends_average = friends_score / len(friends_user_objects)
        # twitter_score = ((friends_average + friends_count) / 2 ) * content_score
        # user = tweets[0].get("user")
        # user["twitter_score"] = twitter_score
        # cache.set(screen_name, user, timeout=86400)
    # return JsonResponse(user)


def get_friends(screen_name):
    # This gets you 5,000 user ids. Use friends.get("next_cursor") to get next page.
    friends = client.request('https://api.twitter.com/1.1/friends/ids.json?screen_name='+screen_name)
    return friends.get("ids")


def get_users(user_ids):
    user_ids_as_string = ','.join(map(str, user_ids))
    users = client.request('https://api.twitter.com/1.1/users/lookup.json?user_id='+user_ids_as_string)
    return users


def get_tweet_score(tweet):
    """ Returns list consisting of positive word count, negative word count, and total word count of single tweet. """

    negative_words = cache.get("negative_words")
    positive_words = cache.get("positive_words")
    if negative_words is None or positive_words is None:
        load_word_lists()
    text = tweet.get("text")
    if text:
        text = re.sub('\W', '', text)
        words = text.split(' ')
        pos_count, neg_count = 0, 0
        for word in words:
            for pos in positive_words:
                print type(pos)
                print pos
                if pos in word:
                    pos_count += 1
            for neg in negative_words:
                if neg in word:
                    neg_count += 1
        return [pos_count, neg_count, len(text)]
    else:
        return [0, 0, 0]


def get_friend_score(user_object):
    friends_count = user_object.get("friends_count")
    latest_tweet = user_object.get("status")
    latest_tweet_score = get_tweet_score(latest_tweet)
    content_score = (latest_tweet_score[0] - latest_tweet_score[1]) / latest_tweet_score[2]
    return content_score * friends_count

def load_word_lists():
    wd =  os.path.dirname(__file__)
    nw =  os.path.join(wd, 'word_lists/negative-words.txt')
    pw = os.path.join(wd, 'word_lists/positive-words.txt')
    with open(nw) as file:
        for row in csv.reader(file):
            print row
            if len(row) != 0:
                if row[0] != ";":
                    negative_words.append(row)
    cache.set("negative_words", negative_words)
    with open(pw) as file:
        reader = csv.reader(file)
        for row in csv.reader(file):
            if row[0] != ";":
                positive_words.append(row)
    cache.set("positive_words", positive_words)
