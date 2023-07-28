# Sentiment Analysis Website

A flask app which scrapes a Yelp link and gives a sentiment rating for every review
on the page. After the scraping, a boxplot, histogram, summary statistics, and a
table showing tagging every sentiment with their respective rating.

### Description

The webpage currently has four pages: home page, enter yelp link page, show comments,
and show graphs page. It runs on `127.0.0.1:5000`.

| File Name               | Purpose                                                                                                                                         |
|-------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------|
| `main.py`               | Handles the functionality of the website using Flask.                                                                                           |
| `sentiment_analysis.py` | Scrapes the inputted Yelp page, gives a sentiment rating to every review, and creates a html showcasing every review with its sentiment rating. |
| `visuals.py`            | Creates the boxplots, histograms, and summary statistics for the sentiment ratings collected from the reviews.                                  |
| `templates/form.html`   | Handles the input form which captures the Yelp link provided by the user, producing error messages if neccessary.                               |
| `templates/index.html`  | The front-end for the home page found at `127.0.0.1:5000`.                                                                                      |
| `templates/result.html` | The front-end for the graphs and summary statistics generated from the data collected.                                                          |                                                          |
| `templates/table.html`  | The front-end for the table showcasing every review with its respective sentiment rating. Generated in `sentiment_analysis.py`                  |
| `requirements.txt`      | Showcases every external package needed (via install) in order for this project to work properly.                                               |
| `secret_key.txt`        | A file the user needs to create and put a random string to ensure that flash messages work while running (this file must be private)            |

### Requirements

The following packages are required in order to run the code (also mentioned in `requirements.txt`):
<ul>
    <li>Flask</li>
    <li>Numpy</li>
    <li>Pandas</li>
    <li>Matplotlib</li>
    <li>Seaborn</li>
    <li>Transformers</li>
    <li>Torch</li>
    <li>Pandas</li>
    <li>Requests</li>
    <li>bs4 (Beautiful Soup)</li>
</ul>

The following can be downloaded using pip for example `pip install flask`.