from flask import Flask, render_template, request, url_for, redirect
import sentiment_analysis

app = Flask(__name__)


@app.route('/')
def home_page():
    return render_template('index.html')


@app.route('/get_yelp_link', methods=["GET", "POST"])
def get_yelp_link():
    if request.method == "POST":
        link = request.form.get('link')
        # return show_sentiment(df)
        sentiment_analysis.initiate(link)
        return redirect(url_for("show_sentiment"))
    else:
        return render_template('form.html')


@app.route('/show_sentiment')
def show_sentiment():
    return render_template('table.html')


if __name__ == "__main__":
    app.run(debug=True)
