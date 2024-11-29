from fastapi import FastAPI, Body, Query, HTTPException
from pydantic import BaseModel
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()

# Simulated in-memory database
users_data = []

class User(BaseModel):
    name: str

@app.get("/home", summary="Fetch all users")
def welcome_server():
    return {"user_data": users_data}

@app.get("/home/{user_class}", summary="Welcome with parameters")
def welcome_with_parameters(user_class: int, query: str = Query(..., description="Query parameter")):
    return {"name": "Bagumire", "class": user_class, "query": query}

@app.put("/username/{user_name}", summary="Add username")
def put_data(user_name: str):
    logging.info(users_data)
    users_data.append(user_name)
    return {"usernames": user_name}

@app.post("/postdata", summary="Add a new user")
def post_data(user: User):
    users_data.append(user.name)
    return {"usernames": users_data}

@app.delete("/delete/{user_name}", summary="Delete a user by username")
def delete_data(user_name: str):
    try:
        users_data.remove(user_name)
        return {"message": f"{user_name} successfully removed.", "data": users_data}
    except ValueError:
        raise HTTPException(status_code=404, detail=f"{user_name} not found.")
