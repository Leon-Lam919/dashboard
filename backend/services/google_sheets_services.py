from google.auth import credentials
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google.auth import credentials
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import datetime
import time as time


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

TASK_COLUMNS={
    "keyboard": "B",
    "code": "C",
    "workout": "D",
    "cardio": "E",
}


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


def pad_row(row, cols):
    return row + [""] * (cols - len(row))

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

    api_call = (
            service.spreadsheets().
            values().
            get(spreadsheetId=SPREADSHEET_ID, range=range_name).
            execute()
        )

    results = api_call.get('values',[])

    if not results:
        # Return all tasks as "No"
        list = {task: "No" for task in TASK_COLUMNS.keys()}
        return list

    results = [pad_row(result, 4) for result in results]

    values_list = results[0]
    result_dict={}
    for i in range(len(values_list)):
        if values_list[i] == '':
            values_list[i] = 'No'

    for index, (task_name, _) in enumerate(TASK_COLUMNS.items()):
        result_dict[task_name] = values_list[index]

    return result_dict

