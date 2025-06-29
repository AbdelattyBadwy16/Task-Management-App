from fastapi import FastAPI
from .database import create_tables
from .routers import router as task_router

app = FastAPI(
    title="Task Management API",
    description="API to manage tasks with FastAPI, SQLModel, and SQLite",
    version="1.0.0"
)

# run when server start
@app.on_event("startup")
def on_startup():
    # create db tables
    create_tables()

# add routers
app.include_router(task_router)


@app.get("/", tags=["Root"])
def read_root():
    """
    Returns API info and list of available endpoints.
    """
    return {
        "message": "Welcome to the Task Management API!",
        "endpoints": {
            "Health Check": {
                "method": "GET",
                "path": "/health",
                "description": "Check API health status."
            },
            "List Tasks": {
                "method": "GET",
                "path": "/tasks/",
                "description": "List tasks with pagination.",
                "query_params": {
                    "limit": "Number of items to return (default=10)",
                    "offset": "Number of items to skip (default=0)",
                    "status": "Filter by task status (pending, in_progress, completed).",
                    "priority": "Filter by task priority (low, medium, high)."
                }
            },
            "Create Task": {
                "method": "POST",
                "path": "/tasks/",
                "description": "Create a new task."
            },
            "Get Task by ID": {
                "method": "GET",
                "path": "/tasks/{task_id}",
                "description": "Retrieve a specific task by its ID."
            },
            "Update Task": {
                "method": "PUT",
                "path": "/tasks/{task_id}",
                "description": "Update an existing task."
            },
            "Delete Task": {
                "method": "DELETE",
                "path": "/tasks/{task_id}",
                "description": "Delete a task by its ID."
            },
            "Get Tasks by Status": {
                "method": "GET",
                "path": "/tasks/status/{status}",
                "description": "Retrieve tasks filtered by status (pending, in_progress, completed)."
            },
            "Get Tasks by Priority": {
                "method": "GET",
                "path": "/tasks/priority/{priority}",
                "description": "Retrieve tasks filtered by priority (low, medium, high)."
            },
        }
    }

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok"}
