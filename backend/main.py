from logging import raiseExceptions
from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from google.auth import credentials
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
import datetime
from pydantic import BaseModel
import time as time
from loguru import logger
from contextlib import asynccontextmanager

# from crontab import CronTab
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    if not(os.getenv('SPREADSHEET_ID')):
        logger.critical("spreadsheet Env missing")
        raise RuntimeError('spreadsheet env not configured')

    yield

app = FastAPI(lifespan=lifespan, root_path="/api")

from config import SPREADSHEET_ID
from routers.google_sheets import router as google_sheets_router
from routers.RSS_news import router as news_router

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(google_sheets_router)
app.include_router(news_router)
