from flask import Flask, render_template, make_response, request, jsonify
from datetime import datetime
import tweepy
import config

app = Flask(__name__)
storage = None
twitter_api, analytics_api = config.connect_with_services()


@app.route('/', methods=['GET', 'POST'])
def sentiment_view():

    if request.method == 'GET':
        return render_template('welcome.html')

    if request.method == 'POST':
        data = {}
        data['hashtag'] = '#' + request.form.get("hashtag")
        data['from'] = request.form.get("from")

        errors = {}
        for k, v in data.items():
            if not v:
                errors[k] = "field cannot be empty"

        if errors:
            return jsonify(errors=errors), 400

        total_count = 0
        last_id = 0
        batch_count = 1
        tweets_analysed = []
        # Azure pozwala na wysyłanie maksymalnie 10 dokumentów naraz
        batch_size = 10
        positive = 0
        negative = 0
        neutral = 0
        while batch_count > 0 and total_count < 1000:
            if total_count == 0:
                tweets = tweepy.Cursor(
                    twitter_api.search,
                    tweet_mode='extended',
                    q=data['hashtag'] + ' -filter:retweets',
                    result_type='recent',
                    lang="pl",
                    since=data['from']).items(batch_size)
            else:
                tweets = tweepy.Cursor(
                    twitter_api.search,
                    tweet_mode='extended',
                    q=data['hashtag'] + ' -filter:retweets',
                    result_type='recent',
                    lang="pl",
                    max_id=last_id - 1,
                    since=data['from']).items(batch_size)

            batch_count = 0
            for tweet in tweets:
                batch_count += 1
                created_at = str(tweet.created_at).split(' ')[0]
                last_id = tweet.id
                tweets_analysed.append({"id": tweet.id_str, "content": tweet.full_text, "created_at": created_at})

            results = None
            tweets_to_analyse = [tweet["content"] for tweet in tweets_analysed[total_count:total_count + batch_count]]
            if tweets_to_analyse:
                results = analytics_api.analyze_sentiment(tweets_to_analyse)

            i = 0
            for tweet in tweets_analysed[total_count:total_count + batch_count]:
                sentiment = results[i]['sentiment']
                if sentiment == 'positive':
                    positive += 1
                if sentiment == 'negative':
                    negative += 1
                if sentiment == 'neutral':
                    neutral += 1

                tweet['sentiment'] = sentiment

                i += 1

            total_count += batch_count

        if total_count == 0:
            return render_template('welcome.html', message="Nie ma tweetów z takim hashtagiem!")

        # avg_sentiment = None
        # if max([positive, negative, neutral]) == positive:
        #     avg_sentiment = 'positive'
        # if max([positive, negative, neutral]) == negative:
        #     avg_sentiment = 'negative'
        # if max([positive, negative, neutral]) == neutral:
        #     avg_sentiment = 'neutral'

        positive_percent = round(positive / total_count * 100, 2)
        negative_percent = round(negative / total_count * 100, 2)
        neutral_percent = round(neutral / total_count * 100, 2)

        return render_template('welcome.html', tweets=tweets_analysed[:10], positive_percent=positive_percent,
                negative_percent=negative_percent, neutral_percent=neutral_percent, total_count=total_count)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)