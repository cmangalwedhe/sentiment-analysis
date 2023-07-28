from flask import Flask, render_template, request, url_for, redirect, flash
import sentiment_analysis
import re

app = Flask(__name__)
file_reader = open("secret_key.txt", "r")
app.secret_key = file_reader.read()
file_reader.close()
ready = False


@app.route('/')
def home_page():
    return render_template('index.html')


# we
@app.route('/get_yelp_link', methods=["GET", "POST"])
def get_yelp_link():
    global ready
    if request.method == "POST":
        link = request.form.get('link')

        if not re.match("https://www\\.yelp\\.com/biz/.*", link) or len(link) == 0:
            flash("Please enter a valid Yelp review link. (Must be in the format: https://www.yelp.com/biz/rest-of-url)", "danger")
            return render_template("form.html")

        sentiment_analysis.initiate(link)
        ready = True
        return redirect(url_for("display_graph"))
    else:
        return render_template('form.html')


@app.route('/show_sentiment')
def show_sentiment():
    if not ready:
        flash("In order to view the sentiments for each review, you must provide a valid Yelp link.", "danger")
        return redirect(url_for("get_yelp_link"))

    return render_template('table.html')


@app.route('/display_graph')
def display_graph():
    try:
        import visuals
    except NameError:
        flash("In order to view the graphs, you must provide a valid Yelp link.", "danger")
        return redirect(url_for("get_yelp_link"))

    encoded_boxplot = visuals.generate_graph()
    summary_stats = visuals.generate_summary_statistics()
    return render_template('result.html', encoded_boxplot=encoded_boxplot,
                           encoded_histogram=visuals.generate_histogram(),
                           mean=summary_stats[0], median=summary_stats[1], min=summary_stats[2], max=summary_stats[3],
                           standard_deviation=summary_stats[4])


if __name__ == "__main__":
    app.run(port=5000)
