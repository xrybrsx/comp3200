import json
from ast import keyword
from http import client
from azure.cosmos import CosmosClient
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey

from twitter_api import search_keyword_url, tweets_full_info_url, twitter_auth_and_connect


__ACCOUNT_URI = 'https://comp3200.documents.azure.com:443/'
__ACCOUNT_KEY = 'XdUzJzsysfc7KQAkEKMpXSLqS5tHu2n8dyqC2MtNLpUqRhLDRH5LoVdG6LD3X7yqmKbHURUQDjwRTvZZrz4ynw=='
bearer_token = 'AAAAAAAAAAAAAAAAAAAAACJWYQEAAAAAJ8L97yf%2FLbDoTTQLW77TcQLT8HQ%3D7GqMszwYUwK8lx8GFuhROYpIym8AyWQB0t6e7pEBeSbBBjTgny'


def connectToClient():
    client = CosmosClient(__ACCOUNT_URI, credential=__ACCOUNT_KEY)
    return client

# connect to container in database


def connectToContainer(database_name, container_name):
    client = connectToClient()
    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)
    return container

# put fetched tweets into database table "tweets"


def store_tweets(data, keyword):
    

    container = connectToContainer('tweets', 'tweets')
    data = str(data)
    data = eval(data)
    print(data)
    for i in data['data']:
        item = container.upsert_item({
            "keyword": keyword,
            "id": i['id'],
            "text": i['text'], 
            "source": i['source'],
            "lang": i['lang'],
            "user": i['author_id'],
            "source": i['source'],
            "public_metrics": i["public_metrics"]
        })
        print(item)
        if 'entities' in i:
            if 'hashtags' in i['entities']:
                item['hashtags'] = i['entities']['hashtags']
                container.upsert_item(item)

        if 'context_annotations' in i:
            item['context'] = i['context_annotations']
            container.upsert_item(item)

    return container

# put fetched users into database table "users"


def store_users(data, keyword):
    container = connectToContainer("tweets", 'users')
    data = str(data)
    data = eval(data)
    data = data['includes']
    
    for i in data['users']:
        item = container.upsert_item({
            "keyword": keyword,
            "id": i['id'],
            "username": i['username'],
            "name": i['name'],
        })
        #print(item)
        if 'location' in i:
            print(i)
            item['location'] = i['location']
            container.upsert_item(item)

    return container

# get n tweets from db

# def get_public_metrics(n, keyword):
#     container = connectToContainer('tweets', 'tweets')
#     # item_list = list(container.read_all_items(max_item_count=10))
#     query = "SELECT TOP {} * FROM tweets t WHERE t.keyword = \"{}\"".format(n,keyword)
#     print(query)
#     items = list(container.query_items(
#         query=query,
#         enable_cross_partition_query=True
#     ))

#     return items
def get_tweets(n,keyword):

    # with open('twitter_api_example.json') as json_file:
    #    data = json.load(json_file)
    # return data
    container = connectToContainer('tweets', 'tweets')
    # item_list = list(container.read_all_items(max_item_count=10))
    query = "SELECT TOP {} * FROM tweets t WHERE t.keyword = \"{}\"".format(n,keyword)
    print(query)
    items = list(container.query_items(
        query=query,
        enable_cross_partition_query=True
    ))
    return items

def get_users(n, keyword):
    # with open('twitter_api_example.json') as json_file:
    #    data = json.load(json_file)
    # return data
    container = connectToContainer("tweets", 'users')
    # item_list = list(container.read_all_items(max_item_count=10))
    query = "SELECT TOP {} * FROM users u WHERE u.keyword = \"{}\"".format(n, keyword)

    items = list(container.query_items(
        query=query,
        enable_cross_partition_query=True
    ))
    return items


if __name__ == "__main__":
        
        keyword = "python"
       
        
       # store_users(tweets, keyword)
#     print(get_tweets(100))
#     # with open('twitter_api_example.json') as json_file:
#     #     data = json.load(json_file)
#     # # store_tweets(data)
#     context = {}
#     context["domain"] = []
#     context["entity"] = []
#     df = pd.json_normalize(get_tweets(10))
#     for i in df['context']:
#         if isinstance(i, list):
#             # print(i)
#             for j in i:
#                 # print(j['domain'])
#                 context["domain"].append(j['domain'])
#                 # print(j['entity'])
#                 context["entity"].append(j['entity'])
#             # context = pd.json_normalize(df['context'])
#     print(context)
#     # print(df['context']['enitity'])
#     # for i in data['data']:
#     #     print(i['text'])
#     #     print(i['id'])
#     #     print(i['lang'])
#     #     print(i['source'])
#     #     print(i['author_id'])
#     # for i in data['data']:
#     #     if 'entities' in i:
#     #         if 'hashtags' in i['entities']:
#     #             print(i['entities']['hashtags'])
#     #     if 'context_annotations' in i:
#     #         print(i['context_annotations'])
