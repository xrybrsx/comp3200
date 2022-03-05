from typing import Container
from azure.cosmos import CosmosClient
import json


def connectToClient():
    ACCOUNT_URI = 'https://comp3200.documents.azure.com:443/'
    ACCOUNT_KEY = 'XdUzJzsysfc7KQAkEKMpXSLqS5tHu2n8dyqC2MtNLpUqRhLDRH5LoVdG6LD3X7yqmKbHURUQDjwRTvZZrz4ynw=='
    client = CosmosClient(ACCOUNT_URI, credential=ACCOUNT_KEY)
    return client


def connectToContainer(database_name, container_name):
    client = connectToClient()
    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)
    return container


def store(data):
    container = connectToContainer('tweets', 'tweets')
    for i in data:
        container.upsert_item({
            "text": i['text'],
            "id": i['id']
        })
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
    print(get_tweets(2))
