from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import re


tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')


def get_sentiment_score(review: str) -> int:
    tokens = tokenizer.encode(review, return_tensors='pt')
    result = model(tokens)
    return int(torch.argmax(result.logits)) + 1


def initiate(link):
    yelp_link = link

    r = requests.get(yelp_link)
    soup = BeautifulSoup(r.text, 'html.parser')
    regex = re.compile('.*comment.*')
    results = soup.find_all('p', {'class': regex})
    span_regex = re.compile('\\s*css-chan6m\\s*')
    page_numbers = soup.find_all('span', {'class': span_regex})
    total_pages = -1

    for num in page_numbers:
        if re.match("\\d+ of \\d+", num.text):
            total_pages = num.text

    print(int((total_pages.split(" ")[-1])))
    reviews = [result.text for result in results]

    df = pd.DataFrame(np.array(reviews), columns=['review'])

    df['sentiment'] = df['review'].apply(lambda x: get_sentiment_score((x[:512])))
    return df