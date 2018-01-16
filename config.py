import datetime

CATEGORIES = ['askstories', 'showstories', 'newstories', 'jobstories']
DEFAULT_CATEGORY = 'all'
LOG_FILE = 'hn_parser.log'
RESULTS = 'results'
REPORT = 'report.csv'
FROM_DATE_DEFAULT = datetime.datetime.now() - datetime.timedelta(hours=0.5)
SCORE_DEFAULT = 0
REQUEST_URL_CATEGORY = 'https://hacker-news.firebaseio.com/v0/'
REQUEST_URL_ARTICLE = 'https://hacker-news.firebaseio.com/v0/item/'

