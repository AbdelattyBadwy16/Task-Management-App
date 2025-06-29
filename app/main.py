from fastapi import FastAPI
from dotenv import load_dotenv

# load environment variables from .env file
load_dotenv()

from .database import create_tables
from .routers import router as task_router

# create FastAPI app
app = FastAPI(
    title="Task Management API",
    description="API to manage tasks with FastAPI, SQLModel, and SQLite",
    version="1.0.0"
)

# this runs when the server starts
@app.on_event("startup")
def on_startup():
    # create tables in the database if not exists
    create_tables()

# register all the task routes
app.include_router(task_router)


@app.get("/", tags=["Root"])
def read_root():
    """
    Returns API info and list of available endpoints.
    """
    return {
        "message": "Welcome to the Task Management API!",
        "endpoints": [
            {
                "name": "Health Check",
                "method": "GET",
                "path": "/health",
                "description": "Check API health status."
            },
            {
                "name": "List Tasks",
                "method": "GET",
                "path": "/tasks/",
                "description": "List tasks with filtering, search, sorting and pagination.",
                "query_params": {
                    "limit": "Number of items to return (default=10).",
                    "offset": "Number of items to skip (default=0).",
                    "status": "Filter by status (pending, in_progress, completed).",
                    "priority": "Filter by priority (low, medium, high).",
                    "assigned_to": "Filter by assignee name.",
                    "from_due_date": "Filter tasks with due date >= this date.",
                    "to_due_date": "Filter tasks with due date <= this date.",
                    "search": "Search in title/description.",
                    "order_by": "Field to sort by.",
                    "desc": "Sort descending (true/false)."
                }
            },
            {
                "name": "Create Task",
                "method": "POST",
                "path": "/tasks/",
                "description": "Create a new task."
            },
            {
                "name": "Get Task by ID",
                "method": "GET",
                "path": "/tasks/{task_id}",
                "description": "Retrieve a specific task by its ID."
            },
            {
                "name": "Update Task",
                "method": "PUT",
                "path": "/tasks/{task_id}",
                "description": "Update an existing task."
            },
            {
                "name": "Delete Task",
                "method": "DELETE",
                "path": "/tasks/{task_id}",
                "description": "Delete a task by its ID."
            },
            {
                "name": "Bulk Update Tasks",
                "method": "PUT",
                "path": "/tasks/bulk",
                "description": "Update multiple tasks by IDs."
            },
            {
                "name": "Bulk Delete Tasks",
                "method": "DELETE",
                "path": "/tasks/bulk",
                "description": "Delete multiple tasks by IDs."
            },
            {
                "name": "Get Tasks by Status",
                "method": "GET",
                "path": "/tasks/status/{status}",
                "description": "Retrieve tasks filtered by status."
            },
            {
                "name": "Get Tasks by Priority",
                "method": "GET",
                "path": "/tasks/priority/{priority}",
                "description": "Retrieve tasks filtered by priority."
            },
        ]
    }


# simple health check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok"}
