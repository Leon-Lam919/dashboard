from fastapi import FastAPI, HTTPException, APIRouter
import time as time
from pydantic import BaseModel

from services.google_sheets_services import *
from config import *

app = FastAPI()
router = APIRouter()

service = get_sheets_service()

class updateData(BaseModel):
    status: str

# GET endpoint for frontend to see updated current stats of tasks
@router.get("/get_all")
def get_all():
    try:
        today = check_date(service, SPREADSHEET_ID)
        return get_all_tasks(service, SPREADSHEET_ID, today)
    except Exception as e:
        print("Endpoint get_all ERROR:", e)
        return {}

@router.get("/health")
def health():
    return {"status": "successful", "service":"FastAPI" }

@router.get("/ready")
def ready():
    try:
        result = get_sheets_service()
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))

    if result:
        return {"status": "successful", "service": 'google sheets'}
    else:
        raise HTTPException(status_code=503, detail="google sheets returned empty")


# API endpoint that handles the call from the frontend
# Update the spreadsheet with daily tasks

@router.put("/tasks/{task_id}")
def update_task(task_id: str, data: updateData):

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

    if data.status.lower() not in ["yes", "no"]:
        raise HTTPException(status_code=400, detail="Status must be yes or no")
    
    status = data.status.capitalize()
    row = check_date(service, SPREADSHEET_ID)
    success = update_task_status(service, SPREADSHEET_ID, row, col, status)

    if success:
        return {"success": True, "task": task_id, "status": status}
    else: 
        raise HTTPException(status_code=400, detail="Update could not be made")

app.include_router(router)
