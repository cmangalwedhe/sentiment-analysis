from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import re
from flask import Flask, render_template, request

flask = Flask(__name__)

tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')


def get_sentiment_score(review: str) -> int:
    tokens = tokenizer.encode(review, return_tensors='pt')
    result = model(tokens)
    return int(torch.argmax(result.logits)) + 1

link = 'https://www.yelp.com'


@flask.route('/enter_link', methods=["GET", "POST"])
def enter_link():
    global link

    if request.method == "POST":
        link = request.form['link']
        return "Thank you, please standby!"
    else:
        return render_template('form.html')

if __name__ == "__main__":
    flask.run(debug=True)

    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'html.parser')
    regex = re.compile('.*comment.*')
    results = soup.find_all('p', {'class': regex})
    reviews = [result.text for result in results]

    df = pd.DataFrame(np.array(reviews), columns=['review'])

    df['sentiment'] = df['review'].apply(lambda x: get_sentiment_score((x[:512])))
    print(df)