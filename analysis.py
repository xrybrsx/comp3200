
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import string 
import pandas as pd
from nltk.corpus import stopwords

stopwords = nltk.download('stopwords')



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
     

        pos = pos + pair['positive']
       # print(pos)

        neg = neg + pair['negative']
        # print(neg)

        neu = neu + pair['neutral']
        # print("neutral")
    neu = neu/number
    pos = pos/number 
   
    neg = neg/number 
   
   
    arr = {"positive": pos, "negative": neg}
    return arr



def analyse(data):
    nltk.download('stopwords')
    nltk.download('vader_lexicon')
    text = []
    sentiment_list = []
 
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


    return sentiment_list  

        

def common_words(data, n):
    text = []
    for i in data:
       
        text.append( i["text"])
  
    tmp = []
    
    
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
 
    fd = nltk.FreqDist(tmp)
    
    return fd.most_common(n)
 

