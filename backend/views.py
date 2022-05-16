from .models import UserRegister, LoginOut
from .functions import read_data, show_data

from uuid import UUID
from pydantic import EmailStr
from fastapi import Body, Form, Path

import json


def signup(user: UserRegister = Body(...)):
    """
    Signup
    - This path operation register a user in the app

    Parameters: 
    - Request body parameter
        - user: UserRegister
    Returns a json with the basic user information: 
    - user_id: UUID
    - email: Emailstr
    - first_name: str
    - last_name: str
    - birth_date: datetime
    """
    with open("database/users.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        user_dict = user.dict()
        user_dict["user_id"] = str(user_dict["user_id"])
        user_dict["birth_date"] = str(user_dict["birth_date"])
        results.append(user_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return user


def login(email: EmailStr = Form(...), password: str = Form(...)):
    """
    # [Login]
    This path operation login a Person in the app
    ### Parameters:
    - Request body parameters:
        - email: EmailStr
        - password: str
    ### Returns a LoginOut model with username and message
    """
    data = read_data("users")
    for user in data:
        if email == user['email'] and password == user['password']:
            return LoginOut(email=email)
        else:
            return LoginOut(email=email, message="Login Unsuccesfully!")


def show_all_users():
    """
    # [Show all users]
    This path operation shows all user in the app
    ### Parameters
    - 
    ### Returns a json with the all users in the app, with the following keys:
    - user_id: UUID
    - email: EmailStr
    - first_name: str
    - last_name: str
    - birth_date: datetime        
    """
    with open("users.json", "r", encoding="utf-8") as f:
        results = json.loads(f.read())
        return results


def show_a_user(
    user_id: UUID = Path(
        ...,
        title="User_id",
        description="This is the person id"
    )
):
    """
    # [Show a user]
    This path operation show a user in the app
    ### Parameters
    - Request body parameter: 
        - **user_id: UUID**

    ### Returns a json with the a user in the app, with the following keys:
    - user_id: UUID
    - email: EmailStr
    - first_name: str
    - last_name: str
    - birth_date: datetime        
    """
    return show_data("users", user_id, "user")
