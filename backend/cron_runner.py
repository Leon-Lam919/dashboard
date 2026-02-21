import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import date, timedelta

from fastapi.routing import serialize_response

load_dotenv(Path("/home/theo/dashboard/backend/.env"))

from main import get_all_tasks, check_date, update_task_status, get_sheets_service

with open("/home/theo/dashboard/backend/logs/cron_debug.log", "a") as f:
    f.write(f"Script started at {date.today()}\n")

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')

service = get_sheets_service()

TASK_COLUMNS={
    "keyboard": "B",
    "code": "C",
    "workout": "D",
    "cardio": "E",
}

def pad_row(row, cols):
    return row + [""] * (cols - len(row))

def main():
    # check the date, minus one to obtain the previous day, which we want to update
    yesterday = date.today() - timedelta(days=1)
    row = check_date(service, SPREADSHEET_ID, yesterday)

    range_name = f"Dailies!B{row}:E{row}"

    # get all tasks, find the ones that are blank
    api_call = (
            service.spreadsheets().
            values().
            get(spreadsheetId=SPREADSHEET_ID, range=range_name).
            execute()
        )

    results = api_call.get('values',[])
    
    results = [pad_row(result, 4) for result in results]
    row_list = results[0]
    
    for index, key in enumerate(TASK_COLUMNS):
        col = row_list[index]
        if col == '':
            update_task_status(service, SPREADSHEET_ID, row, TASK_COLUMNS[key], 'No')

if __name__ == "__main__":
    main()
