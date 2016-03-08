from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.core.cache import cache

import json, os, pprint, re, csv, calendar, time, datetime, email.utils
from application_only_auth import Client


CONSUMER_KEY = os.environ["CONSUMER_KEY"]
CONSUMER_SECRET = os.environ["CONSUMER_SECRET"]
client = Client(CONSUMER_KEY, CONSUMER_SECRET)

temp_data = []
negative_words = []
positive_words = []

def twitter_data(request, screen_name):
    # Query strings for tweet filter
    picture_toggle = request.GET.get('picture_toggle')
    retweet_count = request.GET.get('retweet_count')
    date_start = float(request.GET.get('date_start', 0))
    date_end = float(request.GET.get('date_end', calendar.timegm(datetime.datetime.utcnow().utctimetuple())))

    # Check if user exists in cache
    user = cache.get(screen_name)
    tweets = cache.get(screen_name+':tweets')

    if user is None or tweets is None:
        tweets = client.request('https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name='+screen_name+'&count=200')
        twitter_score = get_twitter_score(screen_name, tweets)
        user = tweets[0].get("user")
        user["twitter_score"] = twitter_score
        profile_image_url = user.get("profile_image_url")[:-11]+'.png'
        user["profile_image_url"] = profile_image_url
        cache.set(screen_name, user, timeout=86400)
        cache.set(screen_name+':tweets', tweets, timeout=86400)

    tweets_final = []
    # Filter tweets if need be
    for i, tweet in enumerate(tweets):
        media = tweet.get("entities").get("media")
        tweet_created_at = tweet.get("created_at")
        if picture_toggle == "on" and media is None:
            continue
        if picture_toggle == "off" and media is not None:
            continue
        if retweet_count != "all":
            try:
                retweet_count = int(retweet_count)
                if tweet.get("retweet_count") != retweet_count:
                    continue
            except:
                return HttpResponseBadRequest("retweet_count must be 'all' or a number as a string type.")
        if tweet_created_at:
            created_at = float(calendar.timegm(email.utils.parsedate(tweet_created_at)))
            if (created_at < date_start) or (created_at > date_end):
                continue
        tweets_final.append(tweet)

    return JsonResponse({'user': user, 'tweets': tweets_final})


def get_followers(screen_name):
    # This gets you 5,000 user ids. Use followers.get("next_cursor") to get next page.
    followers = client.request('https://api.twitter.com/1.1/followers/ids.json?screen_name='+screen_name+'&count=100')
    return followers.get("ids")


def get_users(user_ids):
    # 100 users per request, 60 per 15 min.. so if we do all 5000, thats 50 requests. Takes up all the requests...
    # Maybe just limit to follower scores to only 100 of them.
    user_ids_as_string = ','.join(map(str, user_ids))
    users = client.request('https://api.twitter.com/1.1/users/lookup.json?user_id='+user_ids_as_string)
    return users


def get_twitter_score(screen_name, tweets):
    content_score = get_content_score(tweets)
    followers_count = tweets[0].get("user").get("followers_count")
    followers_average = get_average_follower_score(screen_name)
    twitter_score = ((followers_average + followers_count) / 2 ) * content_score
    return twitter_score


def get_tweet_score(tweet):
    """ Returns list consisting of positive word count, negative word count, and total word count of single tweet. """
    if tweet:
        negative_words = cache.get("negative_words")
        positive_words = cache.get("positive_words")
        if negative_words is None or positive_words is None:
            load_word_lists()
            negative_words = cache.get("negative_words")
            positive_words = cache.get("positive_words")
        text = tweet.get("text")
        if text:
            text = re.sub('[^a-zA-Z0-9_ ]', '', text)
            words = text.split(' ')
            pos_count, neg_count = 0, 0
            for word in words:
                for pos in positive_words:
                    if pos[0] in word:
                        pos_count += 1
                for neg in negative_words:
                    if neg[0] in word:
                        neg_count += 1
            return [pos_count, neg_count, len(words)]
        else:
            return [0, 0, 0]


def get_content_score(tweets):
    positive_total, negative_total, words_total = 0, 0, 0
    for tweet in tweets:
        score = get_tweet_score(tweet)
        positive_total += score[0]
        negative_total += score[1]
        words_total += score[2]
    content_score = ((positive_total - negative_total) / float(words_total) + 1 )/ 2
    return content_score


def get_follower_score(user_object):
    followers_count = user_object.get("followers_count")
    latest_tweet = user_object.get("status")
    content_score = 0
    if latest_tweet:
        latest_tweet_score = get_tweet_score(latest_tweet)
        content_score = (latest_tweet_score[0] - latest_tweet_score[1]) / float(latest_tweet_score[2])
    return content_score * followers_count


def get_average_follower_score(screen_name):
    followers_ids = get_followers(screen_name)
    followers_user_objects = get_users(followers_ids)
    followers_total_score = 0
    for follower in followers_user_objects:
        cached_follower = cache.get(follower.get("screen_name"))
        if cached_follower:
            followers_total_score += int(cached_follower.get("follower_score"))
        else:
            follower_score = get_follower_score(follower)
            follower["follower_score"] = follower_score
            cache.set(follower.get("screen_name"), follower, timeout=86400)
            followers_total_score += follower_score
    followers_average = followers_total_score / len(followers_user_objects)
    return followers_average


def load_word_lists():
    wd =  os.path.dirname(__file__)
    nw =  os.path.join(wd, 'word_lists/negative-words.txt')
    pw = os.path.join(wd, 'word_lists/positive-words.txt')
    with open(nw) as file:
        for row in csv.reader(file):
            if len(row) != 0 and row[0][0] != ";":
                negative_words.append(row)
    cache.set("negative_words", negative_words)
    with open(pw) as file:
        reader = csv.reader(file)
        for row in csv.reader(file):
            if len(row) != 0 and row[0] != ";":
                positive_words.append(row)
    cache.set("positive_words", positive_words)
