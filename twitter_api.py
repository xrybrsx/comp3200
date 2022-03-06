import requests
import pandas as pd
import json
import yaml
from analysis import authenticate_client, sentiment_analysis as analyse
from analysis import authenticate_client as auth


def create_twitter_url():
    handle = "xrybrsx"
    max_results = 5
    mrf = "max_results={}".format(max_results)
    q = "query=from:{}".format(handle)
    url = "https://api.twitter.com/2/tweets/search/recent?{}&{}".format(
        mrf, q
    )
    return url


# get n tweets by keyword
def search_keyword_url(keyword, n):
    num = "max_results={}".format(n)
    key = "query={}".format(keyword)

    url = "https://api.twitter.com/2/tweets/search/recent?{}&{}".format(
        num, key
    )
    return url

# get n tweets by hashtag


def search_hashtag_url(hashtag, n):
    num = "max_results={}".format(n)
    key = "query=%23{}".format(hashtag)
    url = "https://api.twitter.com/2/tweets/search/recent?{}&{}".format(
        num, key
    )
    return url

# get number of tweets containing a keyword with day granularity


def count_tweets_url(keyword, gran):
    gran = "day"
    granularity = "granularity={}".format(gran)
    key = "query={}".format(keyword)
    url = "https://api.twitter.com/2/tweets/counts/recent?{}&{}".format(
        key, granularity
    )
    return url


def process_yaml():
    with open("config.yaml") as file:
        return yaml.safe_load(file)


def create_bearer_token(data):
    return data["search_tweets_api"]["bearer_token"]


def twitter_auth_and_connect(bearer_token, url):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    response = requests.request("GET", url, headers=headers)
    return response.json()


# def main():
#     keyword = "pole dance"
#     url = search_keyword_url(keyword, 10)
#     data = process_yaml()
#     bearer_token = create_bearer_token(data)
#     res_json = twitter_auth_and_connect(bearer_token, url)
#     print(res_json)

#     client = authenticate_client()
#     # print(tweets(res_json))
#     print(analyse(client, res_json['data']))

# 😂
# if __name__ == "__main__":
#     main()
