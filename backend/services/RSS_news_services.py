import feedparser
from urllib.parse import urlsplit, urlparse
from models.RSS_model import *
import time
import datetime
import calendar
import logging

logger = logging.getLogger(__name__)

RSS_URLS = ['https://feeds.npr.org/1001/rss.xml', 'https://feeds.arstechnica.com/arstechnica/index', 'https://feeds.bbci.co.uk/news/rss.xml?edition=int']
HN_URL= 'https://hnrss.org/frontpage'

def news_outlet(outlet):
    split = urlsplit(outlet).netloc.split(".")

    for source in news:
        if source.value in split:
            return source

    return news.OTHER

def get_news():
    posts = []

    all_posts = []

    for url in RSS_URLS:
        posts.extend(feedparser.parse(url).entries)

    st = time.localtime()

    for post in posts:
        date = post.published_parsed or post.updated_parsed

        if date is None:
            logger.warning('No date found for %s.', post.title)
            continue

        feed = feed_model(title=post.title, description=post.description, link=post.link, date=datetime.datetime.fromtimestamp(calendar.timegm(date)),  source=news_outlet(post.link))
        all_posts.append(feed)


    for entry in feedparser.parse(HN_URL).entries:

        date = entry.published_parsed or entry.updated_parsed

        if date is None:
            logger.warning('No date found for %s.', entry.title)
            continue

        YC = feed_model(title=entry.title, description=None, link=entry.link, date=datetime.datetime.fromtimestamp(calendar.timegm(date)),source=news.YC, comments=entry.comments)
        all_posts.append(YC)

    return all_posts
