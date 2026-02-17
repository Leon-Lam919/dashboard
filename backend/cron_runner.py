import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import date, timedelta

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

def main():
    # check the date, minus one to obtain the previous day, which we want to update
    yesterday = date.today() - timedelta(days=1)
    row = check_date(service, SPREADSHEET_ID, yesterday)

    # get all tasks, find the ones that are blank
    tasks = get_all_tasks(service, SPREADSHEET_ID, row)
    for key, value in tasks.items():
        col = TASK_COLUMNS.get(key)
        if value == 'No':
            print(update_task_status(service, SPREADSHEET_ID, row, col, value))

if __name__ == "__main__":
    main()
