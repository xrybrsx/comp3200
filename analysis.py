
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import string 
import pandas as pd
from nltk.corpus import stopwords

stopwords = nltk.download('stopwords')



# from database import get_tweets
# import json
# __key = "dd9edb553ad6407cadfd24acd47d01a8"
# __endpoint = "https://comp3200.cognitiveservices.azure.com/"


# Authenticate the client using your key and endpoint

# def authenticate_client():
#     ta_credential = AzureKeyCredential(__key)
#     text_analytics_client = TextAnalyticsClient(
#         endpoint=__endpoint,
#         credential=ta_credential)
#     return text_analytics_client


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
# def sentiment_analysis(client, documents):

#     result = client.analyze_sentiment(documents, show_opinion_mining=True)
#     doc_result = [doc for doc in result if not doc.is_error]

#     positive_reviews = [
#         doc for doc in doc_result if doc.sentiment == "positive"]
#     negative_reviews = [
#         doc for doc in doc_result if doc.sentiment == "negative"]
#     neutral_reviews = [
#         doc for doc in doc_result if doc.sentiment == "neutral"]

#     positive_mined_opinions = []
#     mixed_mined_opinions = []
#     negative_mined_opinions = []

#     json_res = []

#     for document in doc_result:
#         text = ''
#         for sentence in document.sentences:
#             text = text + sentence.text
#         # print("--------------------\nText: {}".format(document.sentences))
#         # print("Document Sentiment: {}".format(document.sentiment))
#         # print("Overall scores: positive={0:.2f}; neutral={1:.2f}; negative={2:.2f} \n".format(
#         #     document.confidence_scores.positive,
#         #     document.confidence_scores.neutral,
#         #     document.confidence_scores.negative,
#         # ))
#         json_res.append({"text": text, "sentiment": {"positive": document.confidence_scores.positive,
#                                                      "neutral": document.confidence_scores.neutral,  "negative": document.confidence_scores.negative}})

#     # print(json)
#     return json_res
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


# def analyze(number):
#     tweets = get_tweets(number)
#     texts = []
#     for tw in tweets:
#         texts.append(tw["text"])

#     client = authenticate_client()

#     return sentiment_analysis(client, texts)


def get_sentiment_percentage(data):

    pos = 0
    neg = 0
    neu = 0
    text = []
    for i in data:
       # print(i)
        text.append( i["text"])

    # print(text)
    number = len(data)
   
    temp = analyse(data)
    # print(temp)
    # [{'text': '前半に例として Python の import と C# の using を書いたのを消したんですけどその名残が残っ
    # ちゃいましたね', 'sentiment': {'positive': 0.09, 'neutral': 0.75, 'negative': 0.16}},
    # {'text':...
    # print(temp)
    for pair in temp:
        pair = pair["sentiment"]
        # print(pair)
        # print(pair)
        # print((pair['positive']))

        pos = pos + pair['positive']
       # print(pos)

        neg = neg + pair['negative']
        # print(neg)

        neu = neu + pair['neutral']
        # print("neutral")
    neu = neu/number
    pos = pos/number 
    #pos = pos*2
    neg = neg/number 
    #neg = neg*2
    
    #neu = 1 - (pos+neg)
    
    # neu = neu - half
    # pos = pos+ (half/2)
    # neg= neg + ( half - (half/2))
    arr = {"positive": pos, "negative": neg}
    return arr



def analyse(data):
    nltk.download('stopwords')
    nltk.download('vader_lexicon')
    text = []
    sentiment_list = []
    # sentiment_list["text"] = []
    # sentiment_list["sentiment"] = []
    for i in data:
        
        text.append( i["text"])
        
    
    # print(text)
    stopwords = nltk.corpus.stopwords.words("english")
    sentences = [w for w in text if w.lower() not in stopwords]
    

    
   
    # print(sentences)
    
   
    sia = SentimentIntensityAnalyzer()
    
    for w in sentences:
        #  print(w)
         w = "".join([i for i in w if i not in string.punctuation])
         sentiment = sia.polarity_scores(w)
         sentiment_list.append({"text": w, "sentiment": {"positive": sentiment["pos"], "neutral": sentiment["neu"],  "negative": sentiment["neg"], "compound": sentiment["compound"]+0.01}})

        #  sentiment = sia.polarity_scores(w)
        #  sentiment_list["text"].append(w)
        #  sentiment_list["sentiment"].append(sentiment)

    return sentiment_list  

        

def common_words(data, n):
    text = []
    for i in data:
       
        text.append( i["text"])
    
    # stopwords = nltk.corpus.stopwords.words("english")
    # words = [w for w in text if w.lower() not in stopwords]
    tmp = []
    
        # print("----word-----")
        # print(w)
        #  print(w)
    nltk.download('stopwords') 
    nltk.download('punkt')   
    stop_words = set(nltk.corpus.stopwords.words('english'))
    filtered_sentence = [w for w in text if not w.lower() in stop_words]
    print(filtered_sentence)
    
    
    for w in filtered_sentence :
        #  print(w)
       
        w = "".join([i for i in w if i not in string.punctuation])
        tmp = tmp + nltk.word_tokenize(w)
   
    tmp = [w for w in tmp if len(w)>2]
    tmp = [w.lower() for w in tmp]
    tmp = [w for w in tmp if not w == 'you' and not w == 'the' and not w == 'the' and not w == 'and' and not w == 'for' and not w == 'not' and not w == 'does' and not w == 'have' and not w == 'your' and not w == 'out' and not w == 'that' and not w == 'how' and not w == 'this' and not w == 'all' and not w == 'our' and not w == 'their' and not w == 'my' and not w == 'mine' and not w == 'with' and not w == 'can' and not w == 'only' and not w == 'he' and not w == 'she' and not w == 'her' and not w == 'his' and not w == 'ours' and not w == 'is' and not w == 'will' and not w == 'but' and not w == 'are' and not w == 'more']
  #  print("--------------- tmp_----------______________")
  #  print(tmp) 
    fd = nltk.FreqDist(tmp)
    
    return fd.most_common(n)
    # sentiment_analysis_with_opinion_mining_example(client)


# if __name__ == "__main__":

    # words = common_words(data,10)
   # print(words)

   
#    print(score)
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
