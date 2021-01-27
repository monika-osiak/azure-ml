from flask import Flask, render_template, make_response, request, jsonify
from datetime import datetime
import tweepy
import config
import re

app = Flask(__name__)
storage = None
twitter_api, analytics_api = config.connect_with_services()

RESULT_TRANSLATION = {
    'positive': 'pozytywny',
    'negative': 'negatywny',
    'neutral': 'neutralny'
}

def clean_txt(tweet):
    result = re.sub(r'[#@]', '', tweet)
    result = re.sub(r'https?:\/\/\S+', '', result)
    return result

@app.route('/', methods=['GET', 'POST'])
def sentiment_view():

    if request.method == 'GET':
        return render_template('welcome.html')

    if request.method == 'POST':
        data = {}
        data['hashtag'] = '#' + request.form.get("hashtag")
        data['until'] = request.form.get("until")

        errors = {}
        for k, v in data.items():
            if not v:
                errors[k] = "field cannot be empty"

        if errors:
            return jsonify(errors=errors), 400

        total_count = 0
        tweets_analysed = []
        # Azure pozwala na wysyłanie maksymalnie 10 dokumentów naraz
        batch_size = 10
        positive = 0
        negative = 0
        neutral = 0

        # API Twittera pozwala standardowym użytkownikom pobrać maks 300 twittów przed timeoutem
        tweets = tweepy.Cursor(
            twitter_api.search,
            tweet_mode='extended',
            q=data['hashtag'] + ' -filter:retweets',
            result_type='mixed',
            until=data['until'],
            lang="pl").items(300)

        for tweet in tweets:
            total_count += 1
            created_at = str(tweet.created_at).split(' ')[0]
            last_id = tweet.id
            tweets_analysed.append({"id": tweet.id_str, "author": tweet.author.screen_name, "content": tweet.full_text, "created_at": created_at})

        if total_count == 0:
            return render_template('welcome.html', message="Nie znaleziono tweetów spełniających podane wymagania.")

        for i in range(0, total_count, 10):
            j = i + batch_size
            if j > total_count:
                j = total_count
            
            tweets_to_analyse = [clean_txt(tweet["content"]) for tweet in tweets_analysed[i : j]]
            results = analytics_api.analyze_sentiment(tweets_to_analyse)

            k = 0
            for tweet in tweets_analysed[i : j]:
                sentiment_scores = results[k]['confidence_scores']

                if sentiment_scores.neutral > 0.9:
                    neutral += 1
                    sentiment = 'neutral'
                elif sentiment_scores.positive > sentiment_scores.negative:
                    positive += 1
                    sentiment = 'positive'
                else: 
                    negative += 1
                    sentiment = 'negative'
                
                tweet['sentiment'] = RESULT_TRANSLATION[sentiment]

                k += 1

        positive_percent = round(positive / total_count * 100, 2)
        negative_percent = round(negative / total_count * 100, 2)
        neutral_percent = round(neutral / total_count * 100, 2)

        return render_template('welcome.html', tweets=tweets_analysed[:10], positive_percent=positive_percent,
                negative_percent=negative_percent, neutral_percent=neutral_percent, total_count=total_count)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)