import datetime

CATEGORIES = ('askstories', 'showstories', 'newstories', 'jobstories', 'all')
DEFAULT_CATEGORY = 'jobstories'
LOG_FILE = 'hn_parser.log'
RESULTS = 'results'
REPORT = 'report.csv'
FROM_DATE_DEFAULT = datetime.datetime.now() - datetime.timedelta(hours=0.2)
SCORE_DEFAULT = 0
REQUEST_URL_CATEGORY = 'https://hacker-news.firebaseio.com/v0/'
REQUEST_URL_ARTICLE = 'https://hacker-news.firebaseio.com/v0/item/'
PAYLOAD = {'print': 'pretty'}
ARCHIVE_FILENAME = 'pkl_archive'
DICT_LOG_CONFIG = {
        "version": 1,
        "handlers": {
            "fileHandler": {
                "class": "logging.FileHandler",
                "formatter": "myFormatter",
                "filename": './'+RESULTS+'/'+LOG_FILE
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
