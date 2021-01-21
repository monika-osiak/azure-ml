import tweepy
import csv
import config
from tqdm import tqdm

auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

f = open("hashtags.txt", "r", encoding="utf-8")
for line in tqdm(f):
    hashtag = line[:-1] if line[-1] == '\n' else line
    print('> Parsing ' + hashtag + '...')

    csvFile = open('tweets/' + hashtag[1:] + '.csv', 'w', encoding="utf-8")
    csvWriter = csv.writer(csvFile)

    for tweet in tweepy.Cursor(
            api.search,
            q=hashtag + ' -filter:retweets',
            lang="pl",
            since="2020-01-01"
    ).items(100):
        csvWriter.writerow([tweet.created_at, tweet.text])
