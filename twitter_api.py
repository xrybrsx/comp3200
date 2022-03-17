import requests


# import yaml


def tweets_full_info_url(keyword, n):
    mrf = "max_results={}".format(n)
    q = "query={}".format(keyword)
    url = "https://api.twitter.com/2/tweets/search/recent?{}&expansions=author_id,geo.place_id&{}&tweet.fields=author_id,context_annotations,created_at,entities,id,lang,source,text,withheld,public_metrics&place.fields=country,contained_within,name,place_type,country_code&user.fields=location".format(
        mrf, q
    )
    return url

# get n tweets by username


def tweets_by_user_url(username, n):
    mrf = "max_results={}".format(n)
    q = "query=from:{}".format(username)
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
# {
#     "data": [
#         {
#             "end": "2022-03-01T10:00:00.000Z",
#             "start": "2022-03-01T09:23:24.000Z",
#             "tweet_count": 1186
#         },
#         {
#             "end": "2022-03-01T11:00:00.000Z",
#             "start": "2022-03-01T10:00:00.000Z",
#             "tweet_count": 1998
#         }


def count_tweets_url(keyword, gran):
    gran = "day"
    granularity = "granularity={}".format(gran)
    key = "query={}".format(keyword)
    url = "https://api.twitter.com/2/tweets/counts/recent?{}&{}".format(
        key, granularity
    )
    return url

# get tweet from its id
# returns "data": {
#              "id": "1275828087666679809",
#              "text": "Learn how to create a sentiment score for your Tweets with Microsoft Azure, Python, and Twitter Developer Labs recent search functionality.\nhttps://t.co/IKM3zo6ngu"
#                  }


def get_tweet_url(id):
    url = "https://api.twitter.com/2/tweets/{}".format(id)
    return url

# get my twitter API credentials from a separate file


# def process_yaml():
#     with open("config.yaml") as file:
#         return yaml.safe_load(file)

# # get bearer token for API permissions


# def create_bearer_token(data):
#     return data["search_tweets_api"]["bearer_token"]


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
