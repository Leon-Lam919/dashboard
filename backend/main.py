from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from google.auth import credentials
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')

def get_sheets_service():
    creds = Credentials.from_service_account_file(
        'credentials.json',
        scopes=SCOPES
    )
    service = build('sheets', 'v4', credentials=creds)
    return service
