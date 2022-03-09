from html import entities
from typing import Container
from azure.cosmos import CosmosClient
import json
__ACCOUNT_URI = 'https://comp3200.documents.azure.com:443/'
__ACCOUNT_KEY = 'XdUzJzsysfc7KQAkEKMpXSLqS5tHu2n8dyqC2MtNLpUqRhLDRH5LoVdG6LD3X7yqmKbHURUQDjwRTvZZrz4ynw=='


def connectToClient():
    client = CosmosClient(__ACCOUNT_URI, credential=__ACCOUNT_KEY)
    return client


def connectToContainer(database_name, container_name):
    client = connectToClient()
    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)
    return container


def store_tweets(data):
    container = connectToContainer('tweets', 'tweets')
    for i in data['data']:
        item = container.upsert_item({
            "text": i['text'],
            "id": i['id'],
            "source": i['source'],
            "lang": i['lang'],
            "user": i['author_id'],
            "source": i['source'],
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


def store_users(data):
    container = connectToContainer('tweets', 'users')
    data = data['includes']
    for i in data['users']:
        item = container.upsert_item({
            "user": i['id'],
            "username": i['username'],
            "name": i['name'],
        })
        print(item)
        if 'location' in i:
            item['location'] = i['location']
            container.upsert_item(item)

    return container


def get_tweets(n):
    container = connectToContainer('tweets', 'tweets')
    # item_list = list(container.read_all_items(max_item_count=10))
    query = "SELECT TOP {} * FROM tweets".format(n)

    items = list(container.query_items(
        query=query,
        enable_cross_partition_query=True
    ))
    return items


if __name__ == "__main__":
    with open('twitter_api_example.json') as json_file:
        data = json.load(json_file)
    # store_tweets(data)
    store_users(data)
    # for i in data['data']:
    #     print(i['text'])
    #     print(i['id'])
    #     print(i['lang'])
    #     print(i['source'])
    #     print(i['author_id'])
    # for i in data['data']:
    #     if 'entities' in i:
    #         if 'hashtags' in i['entities']:
    #             print(i['entities']['hashtags'])
    #     if 'context_annotations' in i:
    #         print(i['context_annotations'])
