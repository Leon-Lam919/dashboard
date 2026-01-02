from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from google.auth import credentials
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
import datetime

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')

def get_sheets_service():
    creds = Credentials.from_service_account_file(
        'credentials.json',
        scopes=SCOPES
    )
    service = build('sheets', 'v4', credentials=creds)
    return service

service = get_sheets_service()

# TODO: What does this function need to do:
# Retrieve the google sheets cols
# check if the drop box is " "
# if blank, then return that its blank
# if yes, return complete
# if no, return incomplete

# internal function that checks the row on sheets that 
# reflects today's date and returns that row in the format 'r_#'
def check_date(service, SPREADSHEET_ID, today=None) -> str:

    # finds the date of today
    if today is None:
        today = datetime.date.today()
    result = (
        service.spreadsheets().
        values().
        get(spreadsheetId=SPREADSHEET_ID, range='A2:A400').
        execute()
    )
    rows = result.get("values", [])

    for index, row in enumerate(rows):
        date_str = row[0]
        sheet_date = datetime.datetime.strptime(date_str, "%m/%d/%Y")

        if today == sheet_date.date():
            return f"r_{index+2}"
    raise ValueError(f"Date {today} not found in sheet")

def update_task_status(service, SPREADSHEET_ID, task: str) -> bool:
    return True

@app.get("/test-date")
def test_check_date_endpoint():
    row = check_date(service, SPREADSHEET_ID)
    return {"row": row}













