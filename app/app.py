from flask import Flask, render_template, request, flash, redirect

from textblob import TextBlob
from sys import argv

import easyocr
import cv2


reader = easyocr.Reader(['it'])

def get_text(input_file):
    #img = cv2.imread(input_file)
    #result = reader.readtext(img, detail=0, paragraph=True)
    result = reader.readtext(input_file, detail=0, paragraph=True)
    return result

def get_sentiment(comment, threshold : float = 0.5):
    classifier = TextBlob(comment)
    polarity = classifier.sentiment.polarity
    output_sentiment = 'Positive' if polarity > threshold else 'Negative'
    return output_sentiment

UPLOAD_FOLDER = '/Users/riccardobosio/FlaskForML/FlaskForML/app/files'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

@app.route("/sentiment", methods=['GET', 'POST'])
def predict_sentiment_of_comment():
    request_type_str = request.method
    if request_type_str == 'GET':
        return render_template('sentiment_get.html')
    else:
        text = request.form['text']
        return get_sentiment(text)

@app.route("/ocr", methods=['GET', 'POST'])
def read_image():
    request_type_str = request.method
    if request_type_str == 'GET':
        return render_template('read_image.html')
    else:
        #if 'image' not in request.files:
        #    flash('No file part')
        #    return redirect(request.url)
        try:
            file = request.files['file']
            image = file.read()
        except:
            print("Failing here")
        return get_text(image)