from services.RSS_news_services import get_news
from typing import List
from models.RSS_model import feed_model
from fastapi import FastAPI, HTTPException, APIRouter

app = FastAPI()
router = APIRouter()

@router.get("/news_feed", response_model=List[feed_model])
def news_feed():
    return get_news()

app.include_router(router)
