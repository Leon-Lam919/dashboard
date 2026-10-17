from services.RSS_news_services import news_outlet
from models.RSS_model import news

# base test suite for passing intergrated news outlets

def test_npr_link_maps_to_npr():
    result = news_outlet("https://www.npr.org/2026/10/09/nx-s1-5996890/openai-safety-firings")
    assert result == news.NPR

def test_ars_link_maps_to_ars():
    result = news_outlet("https://arstechnica.com/science/2026/10/neanderthal-wooden-tools-from-spain-found-preserved-in-stone/")
    assert result == news.TECHNICA

def test_bbc_link_maps_to_bbc():
    result = news_outlet("https://www.bbc.com/sport/formula1/articles/cmn4ezn5ep3jo")
    assert result == news.BBC

def test_unknown_link_maps_to_other():
    result = news_outlet("https://google.com/")
    assert result == news.OTHER

def test_blank_link_returns_other():
    result = news_outlet(" ")
    assert result == news.OTHER

