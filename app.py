from flask import Flask, render_template, request
import pandas as pd

from scrape import * 
# from test import * 
from summarise import *

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_news', methods=['POST'])
def get_news():
    if request.method == 'POST':
        
        keywords = request.form.get('keywords')
        pyscrape(keywords)
        main()

        data = pd.read_csv('summaries.csv')
        news_summaries = data['Summary']

        return render_template('result.html', news_summaries=news_summaries)

if __name__ == '__main__':
    app.run(debug=True)
