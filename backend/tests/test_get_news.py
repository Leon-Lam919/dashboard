import time
from types import SimpleNamespace

import feedparser

from services.RSS_news_services import get_news

def make_entry(link):
    """One fake feed entry with every attribute get_news() reads."""
    return SimpleNamespace(
        title="Test story",
        description="Short summary",
        link=link,
        published_parsed=time.gmtime(1_760_000_000),  # a fixed moment, as a struct_time
        comments="https://news.ycombinator.com/item?id=1",
        updated_parsed=None,
    )

def make_entry_no_published(link):
    """One fake feed entry with missing published date attribute get_news() reads."""
    return SimpleNamespace(
        title="Test story",
        description="Short summary",
        link=link,
        published_parsed=None,
        comments="https://news.ycombinator.com/item?id=1",
        updated_parsed=None,
    )


def test_get_news_builds_one_post_per_entry(monkeypatch):

    # Arrange: every feedparser.parse(url) call returns one fake NPR entry
    def fake_parse(url):
        return SimpleNamespace(entries=[make_entry("https://www.npr.org/2026/10/14/test")])

    monkeypatch.setattr(feedparser, "parse", fake_parse)

    # Act
    posts = get_news()

    # Assert: 3 RSS feeds + 1 Hacker News feed, one entry each
    assert len(posts) == 4
    assert posts[0].title == "Test story"
    assert posts[0].source == "npr"

def test_get_news_hacker_news_post(monkeypatch):

    def fake_parse(url):
        return SimpleNamespace(entries=[make_entry("https://www.npr.org/2026/10/14/test")])
    
    monkeypatch.setattr(feedparser, "parse", fake_parse)

    posts = get_news()
    assert posts[-1].source == 'ycCombinator'
    assert posts[-1].comments == "https://news.ycombinator.com/item?id=1"

def test_get_news_unknown_outlet_labeled_other(monkeypatch):
    def fake_parse(url):
        return SimpleNamespace(entries=[make_entry("https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2p4MWNpV0VoR2NvQ0drUC02WEZTZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen")])
    monkeypatch.setattr(feedparser, "parse", fake_parse)

    posts = get_news()
    assert posts[0].source == "other"

def test_skips_entry_with_no_date(monkeypatch):
    def fake_parse(url):
        return SimpleNamespace(entries=[make_entry_no_published("https://www.npr.org/2026/10/14/test"),
                                        make_entry("https://www.npr.org/2026/10/14/test")])
    
    monkeypatch.setattr(feedparser, "parse", fake_parse)

    posts = get_news()
    assert len(posts) == 4



