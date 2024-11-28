from fastapi import FastAPI, Body
from pydantic import BaseModel



app = FastAPI()

users_data = list();

@app.get("/home")
def welcome_server():
    return {
        "user_data": users_data
    }

@app.get("/home/{user_class}")
def welcome_with_parameters(user_class: int, query):
    return {
        "name": "Bagumire",
        "class": user_class,
        "query": query
    }

@app.put("/username/{user_name}")
def putData(user_name: str):
    print(users_data)
    users_data.append(user_name)
    return {
        "usernames": user_name
    }
@app.post("/postdata")
def postData(user_name: str):
    users_data.append(user_name)
    return {
        "usernames": users_data,
    }
@app.delete("/delete/{user_name}")
def deleteData(user_name: str):
    try:
        users_data.remove(user_name)
        print(user_name)
        return (users_data)
    except ValueError:
        print(f"Error: {user_name} not found in users_data list.")
        return {"error": f"{user_name} not found"}
