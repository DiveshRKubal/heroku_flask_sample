from flask import Flask
from flask import request
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import json
import re
from keyword_extraction import extract_phrases_keywords

app = Flask(__name__)


def get_positive_negative_words(ip):
    ip = re.sub(r'[^\w\s]', '', ip)
    test_subset = ip.split()
    sid = SentimentIntensityAnalyzer()
    pos_word_list = []
    neu_word_list = []
    neg_word_list = []

    for word in test_subset:
        if (sid.polarity_scores(word)['compound']) >= 0.5:
            pos_word_list.append(word)
        elif (sid.polarity_scores(word)['compound']) <= -0.5:
            neg_word_list.append(word)
        else:
            neu_word_list.append(word)

    # print('Positive :', pos_word_list)
    # print('Neutral :', neu_word_list)
    # print('Negative :', neg_word_list)
    return (pos_word_list, neg_word_list, neu_word_list)

def sentiment_analysis(ip):
    blob = TextBlob(ip)
    sentiment_score = blob.sentiment

    words = get_positive_negative_words(ip)
    # print(sentiment_score[0])
    if (sentiment_score[0]>0.1):
        sentiment_pol = 'Positive'
    elif (sentiment_score[0]<0):
        sentiment_pol = 'Negative'
    else:
        sentiment_pol = 'Neutral'

    final_sentiment = {'Sentiment':sentiment_pol,
                       'Weightage':str(sentiment_score[0]*100)+'%',
                       'Subjectivity':sentiment_score[1],
                       'Positive Words':words[0],
                       'Negative Words':words[1],
                       'Neutral Words':words[2]}

    final_sentiment = json.dumps(final_sentiment)
    return final_sentiment



@app.route('/sentiment_analysis/')
def extract_sentiment():
    sentence = request.args.get('sentence')
    print('Input Sentence: ', sentence)
    sentiment_result = sentiment_analysis(sentence)
    return sentiment_result


@app.route('/phrases_keyword_extraction')
def extract_keywords_and_phrases():
    sentence = request.args.get('sentence')
    print('Input Sentence: ', sentence)
    phrases_keywords = extract_phrases_keywords(sentence)
    return phrases_keywords


if __name__ == '__main__':
    app.run()
