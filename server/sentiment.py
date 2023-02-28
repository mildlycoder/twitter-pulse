from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
import pandas as pd
import requests
from flask import Flask, jsonify

app = Flask(__name__)

# Here we are loading model and tokenizer
roberta = "cardiffnlp/twitter-roberta-base-sentiment"

model = AutoModelForSequenceClassification.from_pretrained(roberta)
tokenizer = AutoTokenizer.from_pretrained(roberta)

labels = ['Negative', 'Neutral', 'Positive']

# Here we are loading tweets from file
tweets_df = pd.read_csv("tweets.csv")

results = []

for tweet in tweets_df["tweet"]:
    # preprocessing the tweet
    tweet_words = []

    for word in tweet.split(' '):
        if word.startswith('@') and len(word) > 1:
            word = '@user'

        elif word.startswith('http'):
            word = "http"
        tweet_words.append(word)

    tweet_proc = " ".join(tweet_words)

    # Here we are perfomring sentiment analysis
    encoded_tweet = tokenizer(tweet_proc, return_tensors='pt')
    output = model(**encoded_tweet)

    scores = output[0][0].detach().numpy()
    scores = softmax(scores)

    tweet_result = {}

    for i in range(len(scores)):
        l = labels[i]
        s = scores[i]
        tweet_result[l] = s

    results.append(tweet_result)
    
    # print sentiment analysis result
    print(f"Tweet: {tweet}\nSentiment: {tweet_result}\n")


# @app.route('/api/sentiment', methods=['GET'])
# def get_sentiment():
#     global results
    # return jsonify({'results': results})

# @app.route('/', methods=['GET'])
# def get_sentiment():
#     global results
#     response = ""
#     for i, result in enumerate(results):
#         response += f"Tweet {i+1}: {tweets_df.iloc[i]['tweet']}\nSentiment: {result}\n\n"
#     return response

@app.route('/', methods=['GET'])
def get_sentiment():
    global results
    response = "<h1>Sentiment Analysis Results:</h1><br>"
    for i, result in enumerate(results):
        tweet = tweets_df.iloc[i]['tweet']
        sentiment = max(result, key=result.get)
        confidence = result[sentiment]
        response += f"<p><strong>Tweet {i+1}:</strong> {tweet}</p>"
        response += f"<p><strong>Sentiment:</strong> {sentiment}</p>"
        response += f"<p><strong>Confidence:</strong> {confidence:.2f}</p><br>"
    return response


if __name__ == '__main__':
    app.run()
