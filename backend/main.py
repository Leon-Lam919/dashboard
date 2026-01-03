from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google.auth import credentials
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
import datetime

app = FastAPI()

TASK_COLUMNS={
    "keyboard": "B",
    "code": "C",
    "workout": "D",
    "cardio": "E",
}

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

# Buisness logic function
# internal function that checks the row on sheets that 
# reflects today's date and returns that row in the format '#'
def check_date(service, SPREADSHEET_ID, today=None) -> int:

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
            return index+2
    raise ValueError(f"Date {today} not found in sheet")

# Buisness logic function
# handles the operation of updating the right cell with yes or no for complete or incomplete
# returns True or False determined by if the operation went through
def update_task_status(service, SPREADSHEET_ID, row: int, column: str, status: str) -> bool:
    range_name = f"Dailies!{column}{row}"
    try:
        result = service.spreadsheets().values().update(
            spreadsheetId = SPREADSHEET_ID,
            range=range_name,
            valueInputOption="RAW",
            body={"values": [[status]]}
        ).execute()
        
        updated_cells = result.get('updatedCells', 0)
        return updated_cells > 0

    except Exception as e:
        print(f"Error updating cell {e}")
        return False

# API endpoint that handles the call from the frontend
# Update the spreadsheet with daily tasks

@app.put("/tasks/{task_id}")
def update_task(task_id: str, status: str):
    col = TASK_COLUMNS.get(task_id)
    if col is None:
        raise HTTPException(status_code=404, detail="Task not found")

    if status.lower() not in ["yes", "no"]:
        raise HTTPException(status_code=400, detail="Status must be yes or no")
    
    status = status.capitalize()
    row = check_date(service, SPREADSHEET_ID)
    success = update_task_status(service, SPREADSHEET_ID, row, col, status)

    if success:
        return {"success": True, "task": task_id}
    else: 
        raise HTTPException(status_code=400, detail="Update could not be made")

# function that gets all the tasks in today's row and returns as dict
def get_all_tasks(service, SPREADSHEET_ID, row: int) -> dict[str,str]:
    today = check_date(service, SPREADSHEET_ID)
    return {" " : " "}

# GET endpoint for frontend to see updated current stats of tasks
@app.get("/get_all")
def get_all():
    return []

