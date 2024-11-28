from fastapi import FastAPI, Body
from pydantic import BaseModel



app = FastAPI()

users_data = list();

@app.get("/home")
def welcome_server():
    return {
        "name": "Heritier",
        "class": "year 3C",
        "age": "15",

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
def postData(user_name: str, querry):
    users_data.append(user_name)
    return {
        "usernames": users_data,
    }

def deleteData(user_name: str):
    users_data.remove(user_name)
    return {
        "username": users_data
    }
