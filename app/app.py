from flask import Flask, render_template, request

from textblob import TextBlob
from sys import argv


def get_sentiment(comment, threshold : float = 0.5):
    classifier = TextBlob(comment)
    polarity = classifier.sentiment.polarity
    output_sentiment = 'Positive' if polarity > threshold else 'Negative'
    return output_sentiment

app = Flask(__name__)

@app.route("/sentiment", methods=['GET', 'POST'])
def predict_sentiment_of_comment():
    request_type_str = request.method
    if request_type_str == 'GET':
        return render_template('sentiment_get.html')
    else:
        text = request.form['text']
        return get_sentiment(text)