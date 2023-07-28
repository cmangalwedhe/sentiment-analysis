from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import re

tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
global sentiment_list


def get_sentiment_score(review: str) -> int:
    tokens = tokenizer.encode(review, return_tensors='pt')
    result = model(tokens)
    return int(torch.argmax(result.logits)) + 1


def scraping(link):
    r = requests.get(link)
    number_soup = BeautifulSoup(r.text, 'html.parser')

    span_regex = re.compile('\\s*css-chan6m\\s*')
    page_numbers = number_soup.find_all('span', {'class': span_regex})
    total_pages = -1

    for num in page_numbers:
        if re.match("\\d+ of \\d+", num.text):
            total_pages = num.text

    total_pages = int(total_pages.split(" ")[-1])
    reviews = []

    for i in range(0, total_pages * 10, 10):
        if i == 0:
            r = requests.get(link)
        else:
            r = requests.get(f"{link}?start={i}")

        soup = BeautifulSoup(r.text, 'html.parser')
        regex = re.compile('.*comment.*')
        results = soup.find_all('p', {'class': regex})

        for result in results:
            reviews.append(result.text)

    return reviews


def write_html_table(df):
    html_code = """<!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <title>Review Sentiments</title>
      <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css"
        integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    </head>
    <body>
        <ul class="nav justify-content-center">
            <li class="nav-item">
                <a class="nav-link active" href="/">Home Page</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="/get_yelp_link">Enter Link</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="/show_sentiment">Show Comments</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="/display_graph">Show Graphs</a>
            </li>
        </ul>
    </body>\n""" + df.to_html(index=False, justify="left", classes="table table-stripped") + "\n</html>"

    with open("templates/table.html", "w", encoding="utf8", errors="ignore") as f:
        f.write(html_code)


def get_sentiment_list():
    return sentiment_list

def initiate(link):
    reviews = scraping(link)
    df = pd.DataFrame(np.array(reviews), columns=['Review'])

    df['Sentiment'] = df['Review'].apply(lambda x: get_sentiment_score((x[:512])))
    global sentiment_list
    sentiment_list = df['Sentiment']

    write_html_table(df)


