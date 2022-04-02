from dataclasses import dataclass
from database import get_tweets
# from azure.core.credentials import AzureKeyCredential
# from azure.ai.textanalytics import TextAnalyticsClient
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import string 
import pandas as pd
from nltk.corpus import stopwords

stopwords = nltk.download('stopwords')

# from numpy import negative, positive
# import pandas as pd

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
        print(i)
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
    pos = pos/number
    neg = neg/number
    neu = neu/number
    arr = {"positive": pos, "neutral": neu, "negative": neg}
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
    stop_words = set(nltk.corpus.stopwords.words('english'))
    filtered_sentence = [w for w in text if not w.lower() in stop_words]
    print(filtered_sentence)
    filtered_sentence = [w for w in filtered_sentence if len(w)>2]
    print(filtered_sentence)
    for w in filtered_sentence :
        #  print(w)
       
        w = "".join([i for i in w if i not in string.punctuation])
        tmp = tmp + nltk.word_tokenize(w)
   
    tmp = [w for w in tmp if len(w)>2]
    fd = nltk.FreqDist(tmp)
    
    return fd.most_common(n)
    # sentiment_analysis_with_opinion_mining_example(client)


if __name__ == "__main__":

   
    data = [{'created_at': '2022-04-01T07:28:25.000Z', 'text': '#Hadith\n \n#ProphetMuhammad PBUH Said\n\n There is #none who #utters a #supplication, except that #Allah #gives him what he asked, or #prevents #evil from him that is #equal to it as #long as he does not #supplicate for something #evil , or the cutting of ties of the #womb\n\n#Islam', 'source': 'IFTTT', 'public_metrics': {'retweet_count': 0, 'reply_count': 0, 'like_count': 0, 'quote_count': 0}, 'id': '1509794800471527435', 'author_id': '3067395447', 'lang': 'en', 'entities': {'hashtags': [{'start': 0, 'end': 7, 'tag': 'Hadith'}, {'start': 10, 'end': 26, 'tag': 'ProphetMuhammad'}, {'start': 48, 'end': 53, 'tag': 'none'}, {'start': 58, 'end': 65, 'tag': 'utters'}, {'start': 68, 'end': 81, 'tag': 'supplication'}, {'start': 95, 'end': 101, 'tag': 'Allah'}, {'start': 102, 'end': 108, 'tag': 'gives'}, {'start': 131, 'end': 140, 'tag': 'prevents'}, {'start': 141, 'end': 146, 'tag': 'evil'}, {'start': 164, 'end': 170, 'tag': 'equal'}, {'start': 180, 'end': 185, 'tag': 'long'}, {'start': 201, 'end': 212, 'tag': 'supplicate'}, {'start': 227, 'end': 232, 'tag': 'evil'}, {'start': 265, 'end': 270, 'tag': 'womb'}, {'start': 272, 'end': 278, 'tag': 'Islam'}]}}, {'entities': {'mentions': [{'start': 62, 'end': 74, 'username': 'Poshmarkapp', 'id': '357211620'}], 'hashtags': [{'start': 75, 'end': 84, 'tag': 'poshmark'}, {'start': 85, 'end': 93, 'tag': 'fashion'}, {'start': 94, 'end': 100, 'tag': 'style'}, {'start': 101, 'end': 114, 'tag': 'shopmycloset'}, {'start': 115, 'end': 121, 'tag': 'jcrew'}, {'start': 122, 'end': 127, 'tag': 'none'}], 'urls': [{'start': 129, 'end': 152, 'url': 'https://t.co/9zPtkiZYPc', 'expanded_url': 'https://posh.mk/vgj2G0fMRob', 'display_url': 'posh.mk/vgj2G0fMRob'}, {'start': 153, 'end': 176, 'url': 'https://t.co/I5GbPt1LcJ', 'expanded_url': 'https://twitter.com/BrendaDubov/status/1509794775364345861/photo/1', 'display_url': 'pic.twitter.com/I5GbPt1LcJ'}, {'start': 153, 'end': 176, 'url': 'https://t.co/I5GbPt1LcJ', 'expanded_url': 'https://twitter.com/BrendaDubov/status/1509794775364345861/photo/1', 'display_url': 'pic.twitter.com/I5GbPt1LcJ'}, {'start': 153, 'end': 176, 'url': 'https://t.co/I5GbPt1LcJ', 'expanded_url': 'https://twitter.com/BrendaDubov/status/1509794775364345861/photo/1', 'display_url': 'pic.twitter.com/I5GbPt1LcJ'}]}, 'created_at': '2022-04-01T07:28:19.000Z', 'text': "So good I had to share! Check out all the items I'm loving on @Poshmarkapp #poshmark #fashion #style #shopmycloset #jcrew #none: https://t.co/9zPtkiZYPc https://t.co/I5GbPt1LcJ", 'source': 'Poshmark', 'public_metrics': {'retweet_count': 0, 'reply_count': 0, 'like_count': 0, 'quote_count': 0}, 'id': '1509794775364345861', 'author_id': '1420129105224380422', 'lang': 'en', 'context_annotations': [{'domain': {'id': '45', 'name': 'Brand Vertical', 'description': 'Top level entities that describe a Brands industry'}, 'entity': {'id': '781974596706635776', 'name': 'Retail'}}, {'domain': {'id': '46', 'name': 'Brand Category', 'description': 'Categories within Brand Verticals that narrow down the scope of Brands'}, 'entity': {'id': '781974596715024385', 'name': 'Apparel/Accessories'}}, {'domain': {'id': '46', 'name': 'Brand Category', 'description': 'Categories within Brand Verticals that narrow down the scope of Brands'}, 'entity': {'id': '783335558466506752', 'name': 'Online'}}, {'domain': {'id': '47', 'name': 'Brand', 'description': 'Brands and Companies'}, 'entity': {'id': '10040709803', 'name': 'J.Crew'}}, {'domain': {'id': '47', 'name': 'Brand', 'description': 'Brands and Companies'}, 'entity': {'id': '1137017865905684484', 'name': 'Poshmark'}}, {'domain': {'id': '65', 'name': 'Interests and Hobbies Vertical', 'description': 'Top level interests and hobbies groupings, like Food or Travel'}, 'entity': {'id': '844603730221707264', 'name': 'Fashion', 'description': 'Fashion'}}, {'domain': {'id': '66', 'name': 'Interests and Hobbies Category', 'description': 'A grouping of interests and hobbies entities, like Novelty Food or Destinations'}, 'entity': {'id': '846427983237672960', 'name': 'Fashion Brand', 'description': 'Fashion Brand'}}, {'domain': {'id': '45', 'name': 'Brand Vertical', 'description': 'Top level entities that describe a Brands industry'}, 'entity': {'id': '781974596706635776', 'name': 'Retail'}}, {'domain': {'id': '46', 'name': 'Brand Category', 'description': 'Categories within Brand Verticals that narrow down the scope of Brands'}, 'entity': {'id': '781974596715024385', 'name': 'Apparel/Accessories'}}, {'domain': {'id': '47', 'name': 'Brand', 'description': 'Brands and Companies'}, 'entity': {'id': '10040709803', 'name': 'J.Crew'}}, {'domain': {'id': '65', 'name': 'Interests and Hobbies Vertical', 'description': 'Top level interests and hobbies groupings, like Food or Travel'}, 'entity': {'id': '844603730221707264', 'name': 'Fashion', 'description': 'Fashion'}}, {'domain': {'id': '66', 'name': 'Interests and Hobbies Category', 'description': 'A grouping of interests and hobbies entities, like Novelty Food or Destinations'}, 'entity': {'id': '845326060757512192', 'name': 'Fashion Novelty', 'description': 'Fashion Novelty'}}, {'domain': {'id': '67', 'name': 'Interests and Hobbies', 'description': 'Interests, opinions, and behaviors of individuals, groups, or cultures; like Speciality Cooking or Theme Parks'}, 'entity': {'id': '845327283774640128', 'name': 'Fashion Tags', 'description': 'Fashion Blogging'}}]}, {'created_at': '2022-04-01T07:09:05.000Z', 'text': 'MOST TRACKED ALERT : At Fri Apr  1 08:04:19 2022 #None is now 3rd in most tracked list #AvGeek #ADSB https://t.co/3HAsPAAv5a https://t.co/jhd5jp4PIm', 'source': 'FlightAlerts', 'public_metrics': {'retweet_count': 0, 'reply_count': 0, 'like_count': 0, 'quote_count': 0}, 'id': '1509789935238356994', 'author_id': '892059375426297858', 'lang': 'en', 'entities': {'hashtags': [{'start': 49, 'end': 54, 'tag': 'None'}, {'start': 87, 'end': 94, 'tag': 'AvGeek'}, {'start': 95, 'end': 100, 'tag': 'ADSB'}], 'urls': [{'start': 101, 'end': 124, 'url': 'https://t.co/3HAsPAAv5a', 'expanded_url': 'https://www.flightradar24.com/2b580627', 'display_url': 'flightradar24.com/2b580627'}, {'start': 125, 'end': 148, 'url': 'https://t.co/jhd5jp4PIm', 'expanded_url': 'https://twitter.com/Radar_Assistant/status/1509789935238356994/photo/1', 'display_url': 'pic.twitter.com/jhd5jp4PIm'}]}, 'context_annotations': [{'domain': {'id': '45', 'name': 'Brand Vertical', 'description': 'Top level entities that describe a Brands industry'}, 'entity': {'id': '781974597302226944', 'name': 'Transportation'}}]}, {'created_at': '2022-04-01T07:05:21.000Z', 'text': '#Hadith\n \n#ProphetMuhammad PBUH Said\n\n There is #none who #utters a #supplication, except that #Allah #gives him what he asked, or #prevents #evil from him that is #equal to it as #long as he does not #supplicate for something #evil , or the cutting of ties of the #womb\n\n#Islam', 'source': 'IFTTT', 'public_metrics': {'retweet_count': 0, 'reply_count': 0, 'like_count': 0, 'quote_count': 0}, 'id': '1509788992593608704', 'author_id': '100209713', 'lang': 'en', 'entities': {'hashtags': [{'start': 0, 'end': 7, 'tag': 'Hadith'}, {'start': 10, 'end': 26, 'tag': 'ProphetMuhammad'}, {'start': 48, 'end': 53, 'tag': 'none'}, {'start': 58, 'end': 65, 'tag': 'utters'}, {'start': 68, 'end': 81, 'tag': 'supplication'}, {'start': 95, 'end': 101, 'tag': 'Allah'}, {'start': 102, 'end': 108, 'tag': 'gives'}, {'start': 131, 'end': 140, 'tag': 'prevents'}, {'start': 141, 'end': 146, 'tag': 'evil'}, {'start': 164, 'end': 170, 'tag': 'equal'}, {'start': 180, 'end': 185, 'tag': 'long'}, {'start': 201, 'end': 212, 'tag': 'supplicate'}, {'start': 227, 'end': 232, 'tag': 'evil'}, {'start': 265, 'end': 270, 'tag': 'womb'}, {'start': 272, 'end': 278, 'tag': 'Islam'}]}}, {'created_at': '2022-04-01T06:31:10.000Z', 'text': '#Hadith\n \n#ProphetMuhammad PBUH Said\n\n There is #none who #utters a #supplication, except that #Allah #gives him what he asked, or #prevents #evil from him that is #equal to it as #long as he does not #supplicate for something #evil , or the cutting of ties of the #womb\n\n#Islam', 'source': 'Botbird tweets', 'public_metrics': {'retweet_count': 0, 'reply_count': 0, 'like_count': 0, 'quote_count': 0}, 'id': '1509780391133073415', 'author_id': '3067395447', 'lang': 'en', 'entities': {'hashtags': [{'start': 0, 'end': 7, 'tag': 'Hadith'}, {'start': 10, 'end': 26, 'tag': 'ProphetMuhammad'}, {'start': 48, 'end': 53, 'tag': 'none'}, {'start': 58, 'end': 65, 'tag': 'utters'}, {'start': 68, 'end': 81, 'tag': 'supplication'}, {'start': 95, 'end': 101, 'tag': 'Allah'}, {'start': 102, 'end': 108, 'tag': 'gives'}, {'start': 131, 'end': 140, 'tag': 'prevents'}, {'start': 141, 'end': 146, 'tag': 'evil'}, {'start': 164, 'end': 170, 'tag': 'equal'}, {'start': 180, 'end': 185, 'tag': 'long'}, {'start': 201, 'end': 212, 'tag': 'supplicate'}, {'start': 227, 'end': 232, 'tag': 'evil'}, {'start': 265, 'end': 270, 'tag': 'womb'}, {'start': 272, 'end': 278, 'tag': 'Islam'}]}}, {'entities': {'mentions': [{'start': 62, 'end': 74, 'username': 'Poshmarkapp', 'id': '357211620'}, {'start': 80, 'end': 94, 'username': 'uneparisienne', 'id': '57247114'}], 'hashtags': [{'start': 95, 'end': 104, 'tag': 'poshmark'}, {'start': 105, 'end': 113, 'tag': 'fashion'}, {'start': 114, 'end': 120, 'tag': 'style'}, {'start': 121, 'end': 134, 'tag': 'shopmycloset'}, {'start': 135, 'end': 139, 'tag': 'vsx'}, {'start': 140, 'end': 150, 'tag': 'katespade'}, {'start': 151, 'end': 156, 'tag': 'none'}], 'urls': [{'start': 158, 'end': 181, 'url': 'https://t.co/xC9kgSTkSB', 'expanded_url': 'https://posh.mk/y1JtN95HRob', 'display_url': 'posh.mk/y1JtN95HRob'}, {'start': 182, 'end': 205, 'url': 'https://t.co/jBsDaZuNnZ', 'expanded_url': 'https://twitter.com/emporesszia/status/1509780128246628352/photo/1', 'display_url': 'pic.twitter.com/jBsDaZuNnZ'}, {'start': 182, 'end': 205, 'url': 'https://t.co/jBsDaZuNnZ', 'expanded_url': 'https://twitter.com/emporesszia/status/1509780128246628352/photo/1', 'display_url': 'pic.twitter.com/jBsDaZuNnZ'}, {'start': 182, 'end': 205, 'url': 'https://t.co/jBsDaZuNnZ', 'expanded_url': 'https://twitter.com/emporesszia/status/1509780128246628352/photo/1', 'display_url': 'pic.twitter.com/jBsDaZuNnZ'}]}, 'created_at': '2022-04-01T06:30:07.000Z', 'text': "So good I had to share! Check out all the items I'm loving on @Poshmarkapp from @uneparisienne #poshmark #fashion #style #shopmycloset #vsx #katespade #none: https://t.co/xC9kgSTkSB https://t.co/jBsDaZuNnZ", 'source': 'Poshmark', 'public_metrics': {'retweet_count': 0, 'reply_count': 0, 'like_count': 0, 'quote_count': 0}, 'id': '1509780128246628352', 'author_id': '168229443', 'lang': 'en', 'context_annotations': [{'domain': {'id': '45', 'name': 'Brand Vertical', 'description': 'Top level entities that describe a Brands industry'}, 'entity': {'id': '781974596706635776', 'name': 'Retail'}}, {'domain': {'id': '46', 'name': 'Brand Category', 'description': 'Categories within Brand Verticals that narrow down the scope of Brands'}, 'entity': {'id': '781974596807299072', 'name': 'Apparel/Accessories'}}, {'domain': {'id': '46', 'name': 'Brand Category', 'description': 'Categories within Brand Verticals that narrow down the scope of Brands'}, 'entity': {'id': '783335558466506752', 'name': 'Online'}}, {'domain': {'id': '47', 'name': 'Brand', 'description': 'Brands and Companies'}, 'entity': {'id': '10040709801', 'name': 'Kate Spade'}}, {'domain': {'id': '47', 'name': 'Brand', 'description': 'Brands and Companies'}, 'entity': {'id': '1137017865905684484', 'name': 'Poshmark'}}, {'domain': {'id': '65', 'name': 'Interests and Hobbies Vertical', 'description': 'Top level interests and hobbies groupings, like Food or Travel'}, 'entity': {'id': '844603730221707264', 'name': 'Fashion', 'description': 'Fashion'}}, {'domain': {'id': '66', 'name': 'Interests and Hobbies Category', 'description': 'A grouping of interests and hobbies entities, like Novelty Food or Destinations'}, 'entity': {'id': '846427983237672960', 'name': 'Fashion Brand', 'description': 'Fashion Brand'}}, {'domain': {'id': '46', 'name': 'Brand Category', 'description': 'Categories within Brand Verticals that narrow down the scope of Brands'}, 'entity': {'id': '781974596807299072', 'name': 'Apparel/Accessories'}}, {'domain': {'id': '47', 'name': 'Brand', 'description': 'Brands and Companies'}, 'entity': {'id': '10040709801', 'name': 'Kate Spade'}}, {'domain': {'id': '65', 'name': 'Interests and Hobbies Vertical', 'description': 'Top level interests and hobbies groupings, like Food or Travel'}, 'entity': {'id': '844603730221707264', 'name': 'Fashion', 'description': 'Fashion'}}, {'domain': {'id': '66', 'name': 'Interests and Hobbies Category', 'description': 'A grouping of interests and hobbies entities, like Novelty Food or Destinations'}, 'entity': {'id': '845326060757512192', 'name': 'Fashion Novelty', 'description': 'Fashion Novelty'}}, {'domain': {'id': '67', 'name': 'Interests and Hobbies', 'description': 'Interests, opinions, and behaviors of individuals, groups, or cultures; like Speciality Cooking or Theme Parks'}, 'entity': {'id': '845327283774640128', 'name': 'Fashion Tags', 'description': 'Fashion Blogging'}}]}, {'entities': {'mentions': [{'start': 62, 'end': 74, 'username': 'Poshmarkapp', 'id': '357211620'}, {'start': 80, 'end': 93, 'username': 'iheartresale', 'id': '3191532335'}], 'hashtags': [{'start': 94, 'end': 103, 'tag': 'poshmark'}, {'start': 104, 'end': 112, 'tag': 'fashion'}, {'start': 113, 'end': 119, 'tag': 'style'}, {'start': 120, 'end': 133, 'tag': 'shopmycloset'}, {'start': 134, 'end': 139, 'tag': 'none'}, {'start': 140, 'end': 145, 'tag': 'rown'}, {'start': 146, 'end': 157, 'tag': 'backtoback'}], 'urls': [{'start': 159, 'end': 182, 'url': 'https://t.co/VER2sirJSW', 'expanded_url': 'https://posh.mk/XAfpci5HRob', 'display_url': 'posh.mk/XAfpci5HRob'}, {'start': 183, 'end': 206, 'url': 'https://t.co/YjJ71Ym3YE', 'expanded_url': 'https://twitter.com/2000Laralobos/status/1509780078976126981/photo/1', 'display_url': 'pic.twitter.com/YjJ71Ym3YE'}, {'start': 183, 'end': 206, 'url': 'https://t.co/YjJ71Ym3YE', 'expanded_url': 'https://twitter.com/2000Laralobos/status/1509780078976126981/photo/1', 'display_url': 'pic.twitter.com/YjJ71Ym3YE'}, {'start': 183, 'end': 206, 'url': 'https://t.co/YjJ71Ym3YE', 'expanded_url': 'https://twitter.com/2000Laralobos/status/1509780078976126981/photo/1', 'display_url': 'pic.twitter.com/YjJ71Ym3YE'}]}, 'created_at': '2022-04-01T06:29:55.000Z', 'text': "So good I had to share! Check out all the items I'm loving on @Poshmarkapp from @iheartresale #poshmark #fashion #style #shopmycloset #none #rown #backtoback: https://t.co/VER2sirJSW https://t.co/YjJ71Ym3YE", 'source': 'Poshmark', 'public_metrics': {'retweet_count': 0, 'reply_count': 0, 'like_count': 0, 'quote_count': 0}, 'id': '1509780078976126981', 'author_id': '1462061725880971269', 'lang': 'en', 'context_annotations': [{'domain': {'id': '45', 'name': 'Brand Vertical', 'description': 'Top level entities that describe a Brands industry'}, 'entity': {'id': '781974596706635776', 'name': 'Retail'}}, {'domain': {'id': '46', 'name': 'Brand Category', 'description': 'Categories within Brand Verticals that narrow down the scope of Brands'}, 'entity': {'id': '783335558466506752', 'name': 'Online'}}, {'domain': {'id': '47', 'name': 'Brand', 'description': 'Brands and Companies'}, 'entity': {'id': '1137017865905684484', 'name': 'Poshmark'}}, {'domain': {'id': '65', 'name': 'Interests and Hobbies Vertical', 'description': 'Top level interests and hobbies groupings, like Food or Travel'}, 'entity': {'id': '844603730221707264', 'name': 'Fashion', 'description': 'Fashion'}}, {'domain': {'id': '66', 'name': 'Interests and Hobbies Category', 'description': 'A grouping of interests and hobbies entities, like Novelty Food or Destinations'}, 'entity': {'id': '845326060757512192', 'name': 'Fashion Novelty', 'description': 'Fashion Novelty'}}, {'domain': {'id': '67', 'name': 'Interests and Hobbies', 'description': 'Interests, opinions, and behaviors of individuals, groups, or cultures; like Speciality Cooking or Theme Parks'}, 'entity': {'id': '845327283774640128', 'name': 'Fashion Tags', 'description': 'Fashion Blogging'}}]}, {'entities': {'mentions': [{'start': 62, 'end': 74, 'username': 'Poshmarkapp', 'id': '357211620'}, {'start': 80, 'end': 88, 'username': 'SLGKali', 'id': '713625040642650114'}, {'start': 89, 'end': 102, 'username': 'poshmaegan_p', 'id': '82198634'}], 'hashtags': [{'start': 103, 'end': 112, 'tag': 'poshmark'}, {'start': 113, 'end': 121, 'tag': 'fashion'}, {'start': 122, 'end': 128, 'tag': 'style'}, {'start': 129, 'end': 142, 'tag': 'shopmycloset'}, {'start': 143, 'end': 148, 'tag': 'none'}], 'urls': [{'start': 150, 'end': 173, 'url': 'https://t.co/RTtj3XfvEp', 'expanded_url': 'https://posh.mk/vpO6QI3HRob', 'display_url': 'posh.mk/vpO6QI3HRob'}, {'start': 174, 'end': 197, 'url': 'https://t.co/HOyHZcWygp', 'expanded_url': 'https://twitter.com/redreader33/status/1509779991139028999/photo/1', 'display_url': 'pic.twitter.com/HOyHZcWygp'}, {'start': 174, 'end': 197, 'url': 'https://t.co/HOyHZcWygp', 'expanded_url': 'https://twitter.com/redreader33/status/1509779991139028999/photo/1', 'display_url': 'pic.twitter.com/HOyHZcWygp'}, {'start': 174, 'end': 197, 'url': 'https://t.co/HOyHZcWygp', 'expanded_url': 'https://twitter.com/redreader33/status/1509779991139028999/photo/1', 'display_url': 'pic.twitter.com/HOyHZcWygp'}]}, 'created_at': '2022-04-01T06:29:34.000Z', 'text': "So good I had to share! Check out all the items I'm loving on @Poshmarkapp from @SLGKali @poshmaegan_p #poshmark #fashion #style #shopmycloset #none: https://t.co/RTtj3XfvEp https://t.co/HOyHZcWygp", 'source': 'Poshmark', 'public_metrics': {'retweet_count': 0, 'reply_count': 0, 'like_count': 0, 'quote_count': 0}, 'id': '1509779991139028999', 'author_id': '2770910159', 'lang': 'en', 'context_annotations': [{'domain': {'id': '45', 'name': 'Brand Vertical', 'description': 'Top level entities that describe a Brands industry'}, 'entity': {'id': '781974596706635776', 'name': 'Retail'}}, {'domain': {'id': '46', 'name': 'Brand Category', 'description': 'Categories within Brand Verticals that narrow down the scope of Brands'}, 'entity': {'id': '783335558466506752', 'name': 'Online'}}, {'domain': {'id': '47', 'name': 'Brand', 'description': 'Brands and Companies'}, 'entity': {'id': '1137017865905684484', 'name': 'Poshmark'}}, {'domain': {'id': '65', 'name': 'Interests and Hobbies Vertical', 'description': 'Top level interests and hobbies groupings, like Food or Travel'}, 'entity': {'id': '844603730221707264', 'name': 'Fashion', 'description': 'Fashion'}}, {'domain': {'id': '66', 'name': 'Interests and Hobbies Category', 'description': 'A grouping of interests and hobbies entities, like Novelty Food or Destinations'}, 'entity': {'id': '845326060757512192', 'name': 'Fashion Novelty', 'description': 'Fashion Novelty'}}, {'domain': {'id': '67', 'name': 'Interests and Hobbies', 'description': 'Interests, opinions, and behaviors of individuals, groups, or cultures; like Speciality Cooking or Theme Parks'}, 'entity': {'id': '845327283774640128', 'name': 'Fashion Tags', 'description': 'Fashion Blogging'}}]}, {'entities': {'mentions': [{'start': 62, 'end': 74, 'username': 'Poshmarkapp', 'id': '357211620'}], 'hashtags': [{'start': 75, 'end': 84, 'tag': 'poshmark'}, {'start': 85, 'end': 93, 'tag': 'fashion'}, {'start': 94, 'end': 100, 'tag': 'style'}, {'start': 101, 'end': 114, 'tag': 'shopmycloset'}, {'start': 115, 'end': 120, 'tag': 'none'}, {'start': 121, 'end': 134, 'tag': 'gypsywarrior'}, {'start': 135, 'end': 141, 'tag': 'guess'}], 'urls': [{'start': 143, 'end': 166, 'url': 'https://t.co/dpfj9YbHZc', 'expanded_url': 'https://posh.mk/fgQoKtRDRob', 'display_url': 'posh.mk/fgQoKtRDRob'}, {'start': 167, 'end': 190, 'url': 'https://t.co/Eud2mnlqWz', 'expanded_url': 'https://twitter.com/boyd_luttrell/status/1509765209287643136/photo/1', 'display_url': 'pic.twitter.com/Eud2mnlqWz'}, {'start': 167, 'end': 190, 'url': 'https://t.co/Eud2mnlqWz', 'expanded_url': 'https://twitter.com/boyd_luttrell/status/1509765209287643136/photo/1', 'display_url': 'pic.twitter.com/Eud2mnlqWz'}, {'start': 167, 'end': 190, 'url': 'https://t.co/Eud2mnlqWz', 'expanded_url': 'https://twitter.com/boyd_luttrell/status/1509765209287643136/photo/1', 'display_url': 'pic.twitter.com/Eud2mnlqWz'}]}, 'created_at': '2022-04-01T05:30:50.000Z', 'text': "So good I had to share! Check out all the items I'm loving on @Poshmarkapp #poshmark #fashion #style #shopmycloset #none #gypsywarrior #guess: https://t.co/dpfj9YbHZc https://t.co/Eud2mnlqWz", 'source': 'Poshmark', 'public_metrics': {'retweet_count': 0, 'reply_count': 0, 'like_count': 0, 'quote_count': 0}, 'id': '1509765209287643136', 'author_id': '4553874914', 'lang': 'en', 'context_annotations': [{'domain': {'id': '45', 'name': 'Brand Vertical', 'description': 'Top level entities that describe a Brands industry'}, 'entity': {'id': '781974596706635776', 'name': 'Retail'}}, {'domain': {'id': '46', 'name': 'Brand Category', 'description': 'Categories within Brand Verticals that narrow down the scope of Brands'}, 'entity': {'id': '783335558466506752', 'name': 'Online'}}, {'domain': {'id': '47', 'name': 'Brand', 'description': 'Brands and Companies'}, 'entity': {'id': '1137017865905684484', 'name': 'Poshmark'}}, {'domain': {'id': '65', 'name': 'Interests and Hobbies Vertical', 'description': 'Top level interests and hobbies groupings, like Food or Travel'}, 'entity': {'id': '844603730221707264', 'name': 'Fashion', 'description': 'Fashion'}}, {'domain': {'id': '66', 'name': 'Interests and Hobbies Category', 'description': 'A grouping of interests and hobbies entities, like Novelty Food or Destinations'}, 'entity': {'id': '845326060757512192', 'name': 'Fashion Novelty', 'description': 'Fashion Novelty'}}, {'domain': {'id': '67', 'name': 'Interests and Hobbies', 'description': 'Interests, opinions, and behaviors of individuals, groups, or cultures; like Speciality Cooking or Theme Parks'}, 'entity': {'id': '845327283774640128', 'name': 'Fashion Tags', 'description': 'Fashion Blogging'}}]}, {'entities': {'mentions': [{'start': 62, 'end': 74, 'username': 'Poshmarkapp', 'id': '357211620'}, {'start': 80, 'end': 94, 'username': 'jbpl_nrosales', 'id': '175601161'}], 'hashtags': [{'start': 95, 'end': 104, 'tag': 'poshmark'}, {'start': 105, 'end': 113, 'tag': 'fashion'}, {'start': 114, 'end': 120, 'tag': 'style'}, {'start': 121, 'end': 134, 'tag': 'shopmycloset'}, {'start': 135, 'end': 140, 'tag': 'none'}, {'start': 141, 'end': 153, 'tag': 'mallybeauty'}, {'start': 154, 'end': 159, 'tag': 'nike'}], 'urls': [{'start': 161, 'end': 184, 'url': 'https://t.co/IrJU1xunWF', 'expanded_url': 'https://posh.mk/3NNhOXMDRob', 'display_url': 'posh.mk/3NNhOXMDRob', 'status': 200, 'title': "Kat's Shares on Poshmark - @kitikats_kloset", 'description': "Shop Kat's shares on Poshmark. Buy new and gently used designer brands at a discount. Follow Kat's closet.", 'unwound_url': 'https://posh.mk/3NNhOXMDRob'}, {'start': 185, 'end': 208, 'url': 'https://t.co/AxukRrKl1t', 'expanded_url': 'https://twitter.com/Kitikat469/status/1509764952470417410/photo/1', 'display_url': 'pic.twitter.com/AxukRrKl1t'}, {'start': 185, 'end': 208, 'url': 'https://t.co/AxukRrKl1t', 'expanded_url': 'https://twitter.com/Kitikat469/status/1509764952470417410/photo/1', 'display_url': 'pic.twitter.com/AxukRrKl1t'}, {'start': 185, 'end': 208, 'url': 'https://t.co/AxukRrKl1t', 'expanded_url': 'https://twitter.com/Kitikat469/status/1509764952470417410/photo/1', 'display_url': 'pic.twitter.com/AxukRrKl1t'}]}, 'created_at': '2022-04-01T05:29:49.000Z', 'text': "So good I had to share! Check out all the items I'm loving on @Poshmarkapp from @jbpl_nrosales #poshmark #fashion #style #shopmycloset #none #mallybeauty #nike: https://t.co/IrJU1xunWF https://t.co/AxukRrKl1t", 'source': 'Poshmark', 'public_metrics': {'retweet_count': 0, 'reply_count': 0, 'like_count': 0, 'quote_count': 0}, 'id': '1509764952470417410', 'author_id': '275315092', 'lang': 'en', 'context_annotations': [{'domain': {'id': '45', 'name': 'Brand Vertical', 'description': 'Top level entities that describe a Brands industry'}, 'entity': {'id': '781974596706635776', 'name': 'Retail'}}, {'domain': {'id': '46', 'name': 'Brand Category', 'description': 'Categories within Brand Verticals that narrow down the scope of Brands'}, 'entity': {'id': '783335558466506752', 'name': 'Online'}}, {'domain': {'id': '47', 'name': 'Brand', 'description': 'Brands and Companies'}, 'entity': {'id': '10026482869', 'name': 'Nike'}}, {'domain': {'id': '47', 'name': 'Brand', 'description': 'Brands and Companies'}, 'entity': {'id': '1137017865905684484', 'name': 'Poshmark'}}, {'domain': {'id': '46', 'name': 'Brand Category', 'description': 'Categories within Brand Verticals that narrow down the scope of Brands'}, 'entity': {'id': '781974597176467456', 'name': 'Sports/Outdoor'}}, {'domain': {'id': '47', 'name': 'Brand', 'description': 'Brands and Companies'}, 'entity': {'id': '10026482869', 'name': 'Nike'}}, {'domain': {'id': '65', 'name': 'Interests and Hobbies Vertical', 'description': 'Top level interests and hobbies groupings, like Food or Travel'}, 'entity': {'id': '844603730221707264', 'name': 'Fashion', 'description': 'Fashion'}}, {'domain': {'id': '66', 'name': 'Interests and Hobbies Category', 'description': 'A grouping of interests and hobbies entities, like Novelty Food or Destinations'}, 'entity': {'id': '845326060757512192', 'name': 'Fashion Novelty', 'description': 'Fashion Novelty'}}, {'domain': {'id': '67', 'name': 'Interests and Hobbies', 'description': 'Interests, opinions, and behaviors of individuals, groups, or cultures; like Speciality Cooking or Theme Parks'}, 'entity': {'id': '839543390668673024', 'name': 'Fashion'}}, {'domain': {'id': '67', 'name': 'Interests and Hobbies', 'description': 'Interests, opinions, and behaviors of individuals, groups, or cultures; like Speciality Cooking or Theme Parks'}, 'entity': {'id': '845327283774640128', 'name': 'Fashion Tags', 'description': 'Fashion Blogging'}}]}]

    words = common_words(data,10)
    print(words)

   
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
