from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import re
import lxml.html
import lxml.html.clean


tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')


def get_sentiment_score(review: str) -> int:
    tokens = tokenizer.encode(review, return_tensors='pt')
    result = model(tokens)
    return int(torch.argmax(result.logits)) + 1


def initiate(link):
    yelp_link = link

    r = requests.get(yelp_link)
    number_soup = BeautifulSoup(r.text, 'html.parser')

    span_regex = re.compile('\\s*css-chan6m\\s*')
    page_numbers = number_soup.find_all('span', {'class': span_regex})
    total_pages = -1

    for num in page_numbers:
        if re.match("\\d+ of \\d+", num.text):
            total_pages = num.text

    total_pages = int(total_pages.split(" ")[-1])
    reviews = []

    for i in range(0, total_pages*10, 10):
        if i == 0:
            r = requests.get(yelp_link)
        else:
            r = requests.get(f"{yelp_link}&start={i}")

        soup = BeautifulSoup(r.text, 'html.parser')
        regex = re.compile('.*comment.*')
        results = soup.find_all('p', {'class': regex})

        for result in results:
            reviews.append(result.text)

    df = pd.DataFrame(np.array(reviews), columns=['review'])

    df['sentiment'] = df['review'].apply(lambda x: get_sentiment_score((x[:512])))
    html_code = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Results</title>
</head>\n""" + df.to_html() + "\n</html>"

    with open("templates/table.html", "w", encoding="utf8", errors="ignore") as f:
        f.write(html_code)

    # return "NANN HESARA ROMEO!"