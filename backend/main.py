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


def check_date(service, SPREADSHEET_ID, today=None) -> int:

    """
    Buisness logic function
    Find the row number matching the given date.
    
    Args:
        service: Google Sheets API service
        sheet_id: Spreadsheet ID to search
        today: Date to find (defaults to today)
    
    Returns:
        Row number where date was found
    """
    
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


def update_task_status(service, SPREADSHEET_ID, row: int, column: str, status: str) -> bool:

    """
    Buisness logic function
    Updates the cell in the sheet with yes or no

    Args:
        service: Google Sheets API service
        sheet_id: Spreadsheet ID to search
        row: row of the sheet that corresponds with the date
        column: the task that is being marked
    
    Returns:
        true/false if the operation was successful
    """
    
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

    """
    Update a task's completion status for today.
    
    Finds today's row in the spreadsheet and updates the specified
    task column with "Yes" (complete) or "No" (incomplete).
    
    Args:
        task_id (str): Task identifier - keyboard, code, workout, or cardio
        status (str): "yes" or "no" (case-insensitive)
    
    Returns:
        dict: {"success": True, "task": task_id}
    
    Raises:
        HTTPException: 
            - 404: task_id not valid
            - 400: status not yes/no, or update failed
    """

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
    """
    Returns a dict of the current tasks and their status
    
    Args:
        row (int): the row to read from
    
    Returns:
        dict: {"keyboard": Yes/No, "code": yes/no, etc.}
    
    Raises:
        return {task: "No" for task in TASK_COLUMNS.keys()}
    """

    range_name = f"Dailies!B{row}:E{row}"

    result = (
            service.spreadsheets().
            values().
            get(spreadsheetId=SPREADSHEET_ID, range=range_name).
            execute()
        )

    result = result.get('values',[])

    if not result:
        # Return all tasks as "No"
        return {task: "No" for task in TASK_COLUMNS.keys()}

    values_list = result[0]

    result_dict={}
    for i in range(len(values_list)):
        if values_list[i] == '':
            values_list[i] = 'No'

    print(values_list)
    for index, (task_name, _) in enumerate(TASK_COLUMNS.items()):
        result_dict[task_name] = values_list[index]

    return result_dict

# GET endpoint for frontend to see updated current stats of tasks
@app.get("/get_all")
def get_all():
    try:
        today = check_date(service, SPREADSHEET_ID)
        return get_all_tasks(service, SPREADSHEET_ID, today)
    except Exception as e:
        print("ERROR:", e)
        return {}

