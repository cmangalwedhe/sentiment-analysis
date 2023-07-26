from flask import Flask, render_template, request, redirect, url_for
import sentiment_analysis

app = Flask(__name__)


@app.route('/get_yelp_link', methods=["GET", "POST"])
def get_yelp_link():
    if request.method == "POST":
        link = request.form.get('link')
        df = sentiment_analysis.initiate(link)
        return show_sentiment(df)
    else:
        return render_template('form.html')


@app.route('/show_sentiment')
def show_sentiment(result=None):
    string = ""

    for index in result.index:
        string += f"{result['review'][index]} {result['sentiment'][index]}<br><br>"

    return string


if __name__ == "__main__":
    app.run(debug=True)