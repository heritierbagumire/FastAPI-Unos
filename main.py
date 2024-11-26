from fastapi import FastAPI


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

def put_data(user_name):
    return {
        "name": user_name,
        "age": 23,
        users_data.append(user_name): users_data
    }
