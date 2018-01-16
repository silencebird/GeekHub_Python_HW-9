import requests
import argparse
import logging
import logging.config
import json
import pickle
import os
from config import *
from jinja2 import Environment, FileSystemLoader


if not (os.path.exists('results')):
    os.makedirs('results')

dictLogConfig = {
    "version": 1,
    "handlers": {
        "fileHandler": {
            "class": "logging.FileHandler",
            "formatter": "myFormatter",
            "filename": './' + RESULTS + '/' + LOG_FILE
        }
    },
    "loggers": {
        "Parser": {
            "handlers": ["fileHandler"],
            "level": "INFO",
        }
    },
    "formatters": {
        "myFormatter": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    }
}


class HackerNews(object):
    def __init__(self, category_url):
        self.logger = logging.getLogger("Parser")
        self.article_data = {}
        self.article_id = []
        self.category_url = category_url

    # launch logger
    def start_logger(self, dictLogConfig):
        logging.config.dictConfig(dictLogConfig)
        self.logger.info("Program started")

    # parse category using argparse, default = 'all'
    def parse_category(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--category', default=DEFAULT_CATEGORY, choices=CATEGORIES + ['all'])
        self.logger.info("Choose category %s" % parser.parse_args().category)
        if parser.parse_args().category == 'all':
            for category in CATEGORIES:
                self.get_category_data(category)
        else:
            self.get_category_data(parser.parse_args().category)

    # get article unique articles id's
    def get_articles_id(self, current_ids):
        if os.path.isfile('./data.pkl') and not self.article_id:
            pkl_file = open('./data.pkl', 'rb')
            self.article_id = pickle.load(pkl_file)
            pkl_file.close()
            self.article_id = list(set(self.article_id) | set(current_ids))
            return self.article_id

        if not self.article_id:
            self.article_id.extend(current_ids)
            return self.article_id
        else:
            new_ids = list(set(current_ids) - set(self.article_id))
            self.article_id.extend(new_ids)
            output = open('./data.pkl', 'ab')
            pickle.dump(self.article_id, output)
            output.close()
            return new_ids


    # get data from hacker news by article id
    def get_category_data(self, category):
        payload = {'print': 'pretty'}
        self.logger.info(REQUEST_URL_CATEGORY + category + '.json')
        try:
            response = requests.get(self.category_url + category + '.json',
                                    params=payload, timeout=5)
        except ValueError:
            self.logger.error("Request %s error" % ValueError)
            print("Oops! Something wrong. Try again... ", ValueError)

        response.encoding = 'UTF-8'
        #Python articles ids serialization
        ids = self.get_articles_id(json.loads(response.content))
        self.logger.info("Got request %s" % response.content)
        self.logger.info("Create a report file %s" % REPORT)
        self.logger.info('Start filter articles(not older - %s; score >= %s)' % (FROM_DATE_DEFAULT, SCORE_DEFAULT))
        # Looping over articles
        index = 0
        print(len(ids))
        for i in ids:
            index += 1
            print(index)
            try:
                article_text = (requests.get(REQUEST_URL_ARTICLE + str(i) + '.json', params=payload, timeout=5))
            except ValueError:
                self.logger.error("Request %s error" % ValueError)
                print("Oops! Something wrong. Try again...", ValueError)
            current_article = json.loads(article_text.content)
            if datetime.datetime.fromtimestamp(current_article['time']) >= FROM_DATE_DEFAULT:
                    if (current_article['score']) >= SCORE_DEFAULT:
                        current_article['time'] = str(datetime.datetime.fromtimestamp(current_article['time']))
                        self.article_data.setdefault(category, []).append(current_article)


    # Creating HTML file from template using jinja2
    def render_template(self, template_filename, context):
        path = os.path.dirname(os.path.abspath(__file__))
        template_environment = Environment(
            autoescape=False,
            loader=FileSystemLoader(os.path.join(path, 'templates')),
            trim_blocks=False)
        return template_environment.get_template(template_filename).render(context)

    def create_index_html(self):
        fname = "output.html"
        context = {
            'articles': self.article_data
        }
        with open(fname, 'w', encoding="utf-8") as f:
            html = self.render_template('index.html', context)
            f.write(html)


articles = HackerNews(REQUEST_URL_CATEGORY)
articles.start_logger(dictLogConfig)
articles.parse_category()
articles.create_index_html()
print(articles.article_data)
