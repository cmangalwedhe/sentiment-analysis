import matplotlib.pyplot as plt
import numpy as np
import base64
from io import BytesIO
import sentiment_analysis
import seaborn as sns

data = sentiment_analysis.get_sentiment_list()


def generate_graph():
    """
    This method creates a boxplot with the sentiment ratings collected for all reviews on the Yelp page.
    :return: an encoded image of the boxplot to render on the HTML page
    """

    boxplot = sns.boxplot(data, orient="h", color=sns.color_palette()[0])
    boxplot.set(yticklabels=[])

    plt.xlabel("Sentiment Distribution")
    plt.ylabel("Reviews")
    plt.xticks(np.arange(0, 6, 1))
    plt.title("Boxplot Distribution of Sentiments")

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    encoded_image = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()

    return encoded_image


def generate_histogram():
    """
        This method creates a histogram with the sentiment ratings collected for all reviews on the Yelp page.
        :return: an encoded image of the histogram to render on the HTML page
    """

    bins = [i for i in range(0, 6, 1)]
    plt.xticks(np.arange(0, 6, 1))

    plt.title("Histogram of Sentiments Collected from Yelp Reviews")
    plt.hist(data, bins=bins, color=sns.color_palette()[0], ec="black")
    plt.xlabel("Sentiment Rating")
    plt.ylabel("Counts")

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    encoded_image = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()

    return encoded_image


def generate_summary_statistics():
    """
    Generates the following statistics from the sentiments collected: mean, median, minimum, maximum, and standard
    deviation
    :return: a list containing the summary statistics for the data collected
    """
    return [np.mean(data), np.median(data), np.min(data), np.max(data), np.std(data)]
