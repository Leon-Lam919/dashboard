import feedparser
from urllib.parse import urlsplit, urlparse
from models.RSS_model import *
import time
import datetime
import calendar

RSS_URLS = ['https://feeds.npr.org/1001/rss.xml', 'https://feeds.arstechnica.com/arstechnica/index', 'https://feeds.bbci.co.uk/news/rss.xml?edition=int']
HN_URL= 'https://hnrss.org/frontpage'

def news_outlet(outlet):
    split = urlsplit(outlet).netloc.split(".")

    for source in news:
        if source.value in split:
            return source

def get_news():
    posts = []

    all_posts = []

    for url in RSS_URLS:
        posts.extend(feedparser.parse(url).entries)

    st = time.localtime()

    for post in posts:
        feed = feed_model(title=post.title, description=post.description, link=post.link, date=datetime.datetime.fromtimestamp(calendar.timegm(post.published_parsed)),  source=news_outlet(post.link))
        all_posts.append(feed)


    for entry in feedparser.parse(HN_URL).entries:
        YC = feed_model(title=entry.title, description=None, link=entry.link, date=datetime.datetime.fromtimestamp(calendar.timegm(entry.published_parsed)),source=news.YC, comments=entry.comments)
        all_posts.append(YC)

    return all_posts

