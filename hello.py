from flask import Flask
from flask import request
from nltk.corpus import sentiwordnet as swn
import pandas as pd
import text_normalizer as tn
import json

app = Flask(__name__)

def sample_text_norm(input_sentence):
    print('*')
    from text_normalizer.text_normalizer_collection_library import chinese_charactor_text_normalizer_collection_2
    print('*')
    input_sentence = "   我在85.33度C買了一杯900──1000元的咖啡    《ohoh》？？ m_m"
    print('*')
    nor_sentence, meta = chinese_charactor_text_normalizer_collection_2.normalize(input_sentence)
    print('*')
    print(nor_sentence)
    print('*')
    return str(nor_sentence)



def sentiment_analysis(input_sentence, verbose=True):
    print('ip: ', input_sentence)
    print('before error')
    # tokenize and POS tag text tokens
    try:
        tagged_text = [(token.text, token.tag_) for token in tn.nlp(input_sentence)]
    except:
        Exception as e: print(e)
    print ('after error')
    print('tagged text', tagged_text)
    pos_score = neg_score = token_count = obj_score = 0
    # get wordnet synsets based on POS tags
    # get sentiment scores if synsets are found
    for word, tag in tagged_text:
        ss_set = None
        if 'NN' in tag and list(swn.senti_synsets(word, 'n')):
            ss_set = list(swn.senti_synsets(word, 'n'))[0]
        elif 'VB' in tag and list(swn.senti_synsets(word, 'v')):
            ss_set = list(swn.senti_synsets(word, 'v'))[0]
        elif 'JJ' in tag and list(swn.senti_synsets(word, 'a')):
            ss_set = list(swn.senti_synsets(word, 'a'))[0]
        elif 'RB' in tag and list(swn.senti_synsets(word, 'r')):
            ss_set = list(swn.senti_synsets(word, 'r'))[0]
        # if senti-synset is found
        if ss_set:
            # add scores for all found synsets
            pos_score += ss_set.pos_score()
            neg_score += ss_set.neg_score()
            obj_score += ss_set.obj_score()
            token_count += 1

    # aggregate final scores
    final_score = pos_score - neg_score
    norm_final_score = round(float(final_score) / token_count, 2)
    final_sentiment = 'positive' if norm_final_score >= 0 else 'negative'
    if verbose:
        norm_obj_score = round(float(obj_score) / token_count, 2)
        norm_pos_score = round(float(pos_score) / token_count, 2)
        norm_neg_score = round(float(neg_score) / token_count, 2)
        # to display results in a nice table
        sentiment_frame = pd.DataFrame([[final_sentiment, norm_obj_score, norm_pos_score,
                                         norm_neg_score, norm_final_score]],
                                       columns=pd.MultiIndex(levels=[['SENTIMENT STATS:'],
                                                                     ['Predicted Sentiment', 'Objectivity',
                                                                      'Positive', 'Negative', 'Overall']],
                                                             labels=[[0, 0, 0, 0, 0], [0, 1, 2, 3, 4]]))
        print(sentiment_frame)

    return str(sentiment_frame)


@app.route('/sentiment_analysis')
def hello_world():
    sentence = request.args.get('sentence')

    print('US: ', sentence)


    res = [
    {
        "id": "bitcoin",
        "name": "Bitcoin",
        "symbol": "BTC",
        "rank": "1",
        "price_usd": "5295.5504633",
        "price_btc": "1.0",
        "24h_volume_usd": "12669322221.2",
        "market_cap_usd": "93569331745.0",
        "available_supply": "17669425.0",
        "total_supply": "17669425.0",
        "max_supply": "21000000.0",
        "percent_change_1h": "0.18",
        "percent_change_24h": "0.48",
        "percent_change_7d": "-0.44",
        "last_updated": "1556438011"
    }]
    
    sentiment_result = sample_text_norm('The food was good')

    res = {'Input_Sentence': sentiment_result}

    return json.dumps(res)

if __name__ == '__main__':
    app.run()
