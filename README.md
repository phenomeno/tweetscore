# tweetscore

Twitter reputation analyzer for Checkr. tweetscore allows you to view a user's latest tweets. It also allows you to filter for tweets with a certain number of retweets, between dates, and tweets with or without a picture. Additionally, a twitter score is calculated that shows the reputation of a user.

## Stack

Django 1.9.3 for the backend, Angular 1.5 and Bootstrap for the frontend. We also used redis 3.0.7 to cache users and user tweets to avoid exceeding twitter API's rate limits. Apache2 for the web server. Installation of redis is required to run the application properly.

## Scoring strategy

A user's twitter score is calculated from three factors: the number of followers a user has, the content of their tweets, and their followers' score. Since twitter's APIs have rate limits I chose to look at just 100 of a user's followers since that is the number of user objects you can receive as a batch using the [users/lookup endpoint](https://dev.twitter.com/rest/reference/get/users/lookup). You get just 60 of these per 15 minutes, so it would impossible to continually query a follower's followers and so on within the rate limits.

To prevent propagation, a follower's score is calculated with just two factors: the number of followers the follower itself has and the content of their latest tweet.

### Followers count

The number of followers a user has was considered linearly. The more followers you have, the greater your reputation.

### Tweet content score

Content score was determined by using a list of [positive](https://github.com/jeffreybreen/twitter-sentiment-analysis-tutorial-201107/blob/master/data/opinion-lexicon-English/positive-words.txt) and [negative](https://github.com/jeffreybreen/twitter-sentiment-analysis-tutorial-201107/blob/master/data/opinion-lexicon-English/negative-words.txt) words. The strategy used here was count of positive words subtracted by count of negative words, all over the total count of words. For determining a user's score, the count of positive words, negative words, and total words were summed first before determining the ratio. For finding the content score of a user's follower we simply used his/hers latest tweet to determine the ratio. The ratio can be within -1  and 1. I wanted the ratio to lie between 0 and 2 to prevent the outcome of a negative score so we simply add an extra 1 to the ratio.

### Aggregation

To aggregate for a user's follower, we found the product of the follower's follower count and their latest tweet content score. To aggregate for a user's score, we find the average of the 100 followers we queried. We then find the product of the user's follower count and the user's content score. Finally we average the user's product and the average of the user's followers score. We put equal weights on the user's input and the followers.
