from fastapi import FastAPI, Query, HTTPException, Body
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
import uuid
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize the app
app = FastAPI()

# Simulated in-memory database
users_data = {}

# Pydantic model for user input validation
class User(BaseModel):
    name: str
    country: str
    age: int = Query(..., ge=0, le=120)  # Age must be between 0 and 120

# Custom exception handler for validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )

# Fetch all users with optional pagination
@app.get("/users", summary="Fetch all users with pagination")
def fetch_all_users(skip: int = 0, limit: int = 10):
    users_list = list(users_data.items())[skip : skip + limit]
    return {"total_users": len(users_data), "users": users_list}

# Search for users by name
@app.get("/users/search", summary="Search for users by name")
def search_users(name: str = Query(..., description="Name of the user to search for")):
    matching_users = {k: v for k, v in users_data.items() if name.lower() in v["name"].lower()}
    if not matching_users:
        raise HTTPException(status_code=404, detail="No users found")
    return {"matching_users": matching_users}

# Add a new user
@app.post("/users", summary="Add a new user")
def add_user(user: User):
    user_id = str(uuid.uuid4())  # Generate a unique ID
    if user.name in [u["name"] for u in users_data.values()]:
        logging.warning(f"Attempt to add duplicate user: {user.name}")
        raise HTTPException(status_code=400, detail="User already exists")
    users_data[user_id] = {"name": user.name, "country": user.country, "age": user.age}
    logging.info(f"User {user.name} added successfully")
    return {"message": "User added successfully", "user_id": user_id, "users": users_data}

# Update user details
@app.put("/users/{user_id}", summary="Update user details")
def update_user(user_id: str, user: User):
    if user_id not in users_data:
        raise HTTPException(status_code=404, detail="User not found")
    users_data[user_id] = {"name": user.name, "country": user.country, "age": user.age}
    logging.info(f"User {user_id} updated successfully")
    return {"message": "User updated successfully", "user": users_data[user_id]}

# Delete a user
@app.delete("/users/{user_id}", summary="Delete a user by ID")
def delete_user(user_id: str):
    if user_id in users_data:
        del users_data[user_id]
        logging.info(f"User {user_id} deleted successfully")
        return {"message": f"User {user_id} successfully removed", "users": users_data}
    raise HTTPException(status_code=404, detail="User not found")

# Protected route example
@app.get("/protected", summary="Protected route")
def protected_route(api_key: str = Query(..., description="API Key")):
    if api_key != "secret-key":
        logging.warning("Unauthorized access attempt")
        raise HTTPException(status_code=401, detail="Unauthorized")
    logging.info("Authorized access granted")
    return {"message": "Welcome to the protected route"}

# Root endpoint
@app.get("/", summary="Welcome message")
def root():
    return {"message": "Welcome to the FastAPI User Management System!"}
