from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

from numpy import negative, positive
import pandas as pd

from database import get_tweets
import json
__key = "dd9edb553ad6407cadfd24acd47d01a8"
__endpoint = "https://comp3200.cognitiveservices.azure.com/"


# Authenticate the client using your key and endpoint

def authenticate_client():
    ta_credential = AzureKeyCredential(__key)
    text_analytics_client = TextAnalyticsClient(
        endpoint=__endpoint,
        credential=ta_credential)
    return text_analytics_client


# Example function for detecting sentiment in text


# def sentiment_analysis_example(client, documents):

#     # documents = [
#     #     "I had the best day of my life. I wish you were there with me."]
#     response = client.analyze_sentiment(documents=documents)[0]
#     print("Document Sentiment: {}".format(response.sentiment))
#     print("Overall scores: positive={0:.2f}; neutral={1:.2f}; negative={2:.2f} \n".format(
#         response.confidence_scores.positive,
#         response.confidence_scores.neutral,
#         response.confidence_scores.negative,
#     ))
#     for idx, sentence in enumerate(response.sentences):
#         print("Sentence: {}".format(sentence.text))
#         print("Sentence {} sentiment: {}".format(idx+1, sentence.sentiment))
#         print("Sentence score:\nPositive={0:.2f}\nNeutral={1:.2f}\nNegative={2:.2f}\n".format(
#             sentence.confidence_scores.positive,
#             sentence.confidence_scores.neutral,
#             sentence.confidence_scores.negative,
#         ))


# sentiment_analysis_example(client)

# Example method for detecting opinions in text

# returns json of the form
#  [{'text': 'RT @DigitalEdwyn: How to fight...',
#            'sentiment': {'positive': 0.0, 'neutral': 0.01, 'negative': 0.99}},
#   {'text': "RT @sciences_math: We've got you...',
#            'sentiment': {'positive': 0.05, 'neutral': 0.9, 'negative': 0.05}},
#   {'text': 'RT @DG__SAGA: .@bing announces all-in-ejou...',
#            'sentiment': {'positive': 0.07, 'neutral': 0.9, 'negative': 0.03}}]
def sentiment_analysis(client, documents):

    result = client.analyze_sentiment(documents, show_opinion_mining=True)
    doc_result = [doc for doc in result if not doc.is_error]

    positive_reviews = [
        doc for doc in doc_result if doc.sentiment == "positive"]
    negative_reviews = [
        doc for doc in doc_result if doc.sentiment == "negative"]
    neutral_reviews = [
        doc for doc in doc_result if doc.sentiment == "neutral"]

    positive_mined_opinions = []
    mixed_mined_opinions = []
    negative_mined_opinions = []

    json_res = []

    for document in doc_result:
        text = ''
        for sentence in document.sentences:
            text = text + sentence.text
        # print("--------------------\nText: {}".format(document.sentences))
        # print("Document Sentiment: {}".format(document.sentiment))
        # print("Overall scores: positive={0:.2f}; neutral={1:.2f}; negative={2:.2f} \n".format(
        #     document.confidence_scores.positive,
        #     document.confidence_scores.neutral,
        #     document.confidence_scores.negative,
        # ))
        json_res.append({"text": text, "sentiment": {"positive": document.confidence_scores.positive,
                                                     "neutral": document.confidence_scores.neutral,  "negative": document.confidence_scores.negative}})

    # print(json)
    return json_res
# for sentence in document.sentences:

# for mined_opinion in sentence.mined_opinions:
#     target = mined_opinion.target
#     print("......'{}' target '{}'".format(
#         target.sentiment, target.text))
#     print("......Target score:\n......Positive={0:.2f}\n......Negative={1:.2f}\n".format(
#         target.confidence_scores.positive,
#         target.confidence_scores.negative,
#     ))
# for assessment in mined_opinion.assessments:
#     print("......'{}' assessment '{}'".format(
#         assessment.sentiment, assessment.text))
#     print("......Assessment score:\n......Positive={0:.2f}\n......Negative={1:.2f}\n".format(
#         assessment.confidence_scores.positive,
#         assessment.confidence_scores.negative,
#     ))
# for sentence in document.sentences:
#     print("Sentence: {}".format(sentence.text))
#     print("Sentence sentiment: {}".format(sentence.sentiment))
#     print("Sentence score:\nPositive={0:.2f}\nNeutral={1:.2f}\nNegative={2:.2f}\n".format(
#         sentence.confidence_scores.positive,
#         sentence.confidence_scores.neutral,
#         sentence.confidence_scores.negative,
#     ))
#     for mined_opinion in sentence.mined_opinions:
#         target = mined_opinion.target
#         print("......'{}' target '{}'".format(
#             target.sentiment, target.text))
#         print("......Target score:\n......Positive={0:.2f}\n......Negative={1:.2f}\n".format(
#             target.confidence_scores.positive,
#             target.confidence_scores.negative,
#         ))
#         for assessment in mined_opinion.assessments:
#             print("......'{}' assessment '{}'".format(
#                 assessment.sentiment, assessment.text))
#             print("......Assessment score:\n......Positive={0:.2f}\n......Negative={1:.2f}\n".format(
#                 assessment.confidence_scores.positive,
#                 assessment.confidence_scores.negative,
#             ))

# print("\n")

# analyze the text of n tweets from the database


def analyze(number):
    tweets = get_tweets(number)
    texts = []
    for tw in tweets:
        texts.append(tw["text"])

    client = authenticate_client()

    return sentiment_analysis(client, texts)


def get_sentiment_percentage(number):
    pos = 0
    neg = 0
    neutral = 0
    temp = analyze(number)
    # [{'text': '前半に例として Python の import と C# の using を書いたのを消したんですけどその名残が残っ
    # ちゃいましたね', 'sentiment': {'positive': 0.09, 'neutral': 0.75, 'negative': 0.16}},
    # {'text':...
    # print(temp)
    for pair in temp:
        pair = pair['sentiment']
        # print(pair)
        # print((pair['positive']))

        pos = pos + pair['positive']
       # print(pos)

        neg = neg + pair['negative']
        # print(neg)

        neutral = neutral + pair['neutral']
        # print("neutral")
    pos = pos/number
    neg = neg/number
    neutral = neutral/number
    arr = {"positive": pos, "neutral": neutral, "negative": neg}
    return arr

    # sentiment_analysis_with_opinion_mining_example(client)
# if __name__ == "__main__":
#     df = pd.json_normalize(get_sentiment_percentage(10))

#     # tweets = get_tweets(2)
#     # print(len(tweets))
#     # texts = []
#     # for tw in tweets:
#     #     texts.append(tw["text"])

#     # print(texts)
#     # client = authenticate_client()
#     # docs = ["I love this!", "I hate this!"]
#     # sentiment_analysis(client, texts)
