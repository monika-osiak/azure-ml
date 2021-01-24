from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from os import getenv
from dotenv import load_dotenv
import tweepy

load_dotenv()
TWITTER_CONSUMER_KEY = getenv("TWITTER_CONSUMER_KEY")
TWITTER_CONSUMER_SECRET = getenv("TWITTER_CONSUMER_SECRET")
TWITTER_ACCESS_TOKEN = getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = getenv("TWITTER_ACCESS_TOKEN_SECRET")
AZURE_TEXT_ANALYTICS_ENDPOINT = getenv("AZURE_TEXT_ANALYTICS_ENDPOINT")
AZURE_TEXT_ANALYTICS_KEY = getenv("AZURE_TEXT_ANALYTICS_KEY")


def connect_with_services():
    auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    twitter_api = tweepy.API(auth, wait_on_rate_limit=True)

    ta_credential = AzureKeyCredential(AZURE_TEXT_ANALYTICS_KEY)
    text_analytics_api = TextAnalyticsClient(
        endpoint=AZURE_TEXT_ANALYTICS_ENDPOINT,
        credential=ta_credential)

    return twitter_api, text_analytics_api
