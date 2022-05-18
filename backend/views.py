import json
from datetime import datetime
from uuid import UUID

from fastapi import Body
from fastapi import Form
from fastapi import HTTPException
from fastapi import Path
from fastapi import status
from pydantic import EmailStr

from .functions import delete_data
from .functions import overwrite_data
from .functions import read_data
from .functions import show_data
from .models import LoginOut
from .models import Tweet
from .models import UserRegister


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
    with open("backend/users.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        user_dict = user.dict()
        if str(user_dict["user_id"]) in results[-1]["user_id"] or str(user_dict["email"]) in results[-1]["email"]:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="User already exists")
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
        if email == user["email"] and password == user["password"]:
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
    with open("backend/users.json", "r", encoding="utf-8") as f:
        results = json.loads(f.read())
        return results


def show_a_user(
    user_id: UUID = Path(..., title="User_id",
                         description="This is the person id")
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


def delete_a_user(
    user_id: UUID = Path(..., title="User ID",
                         description="This is the user ID")
):
    """
    # [Delete a User]
    This path operation delete a user in the app
    ### Parameters:
    - user_id: UUID
    ### Returns a json with deleted user data:
    - user_id: UUID
    - email: Emailstr
    - first_name: str
    - last_name: str
    - birth_date: datetime
    """
    return delete_data("users", user_id, "user")


# ////////////////////////////twets//////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////


def home():
    """
    # [Show all tweets]
    This path operation shows all tweets in the app
    ### Parameters
    -
    ### Returns a json with the all tweets in the app, with the following keys:
    - tweet_id: UUID
    - content: str
    - create_at: datetime
    - update_at: Optional[datetime]
    - by: User
    """
    return read_data("tweets")


def post(tweet: Tweet = Body(...)):
    """
    # [Post a tweet]
    This path operation register a tweet in the app
    ### Parameters
    - Request body parameter:
        - **tweet: Tweet**
    ### Returns a json with the basic tweet information:
    - tweet_id: UUID
    - content: str
    - create_at: datetime
    - update_at: Optional[datetime]
    - by: User
    """
    results = read_data("tweets")  # open the file and read the data
    tweet_dict = tweet.dict()
    tweet_dict["tweet_id"] = str(tweet_dict["tweet_id"])
    tweet_dict["created_at"] = str(tweet_dict["created_at"])
    if tweet_dict["updated_at"]:
        tweet_dict["updated_at"] = str(tweet_dict["updated_at"])
    tweet_dict["by"]["user_id"] = str(tweet_dict["by"]["user_id"])
    results.append(tweet_dict)  # adding the new tweet to the file
    overwrite_data("tweets", results)

    return tweet


def show_a_tweet(
    tweet_id: UUID = Path(..., title="Tweet_id",
                          description="This is the tweet")
):
    """
    # [Show a tweet]
    This path operation show a tweet in the app
    ### Parameters
    - Request body parameter:
        - **tweet_id: UUID**

    ### Returns a json with the a user in the app, with the following keys:
    - user_id: UUID
    - email: EmailStr
    - first_name: str
    - last_name: str
    - birth_date: datetime
    """
    return show_data("tweets", tweet_id, "tweet")


def delete_a_tweet(
    tweet_id: UUID = Path(..., title="Twwet ID",
                          description="This is the tweet ID")
):
    """
    # [Delete a Tweet]
    This path operation delete a tweet in the app
    ### Parameters:
    - tweet_id: UUID
    ### Returns a json with deleted tweet data:
    - tweet_id: UUID
    - content: str
    - create_at: datetime
    - update_at: Optional[datetime]
    - by: User
    """
    return delete_data("tweets", tweet_id, "tweet")


def update_a_tweet(
    tweet_id: UUID = Path(
        ...,
        title="Tweet ID",
        description="This is the tweet ID",
        example="3fa85f64-5717-4562-b3fc-2c963f66afa9",
    ),
    content: str = Form(
        ...,
        min_length=1,
        max_length=256,
        title="Tweet content",
        description="This is the content of the tweet",
    ),
):
    """
    Update Tweet
    This path operation update a tweet information in the app and save in the database
    Parameters:
    - tweet_id: UUID
    - content: str

    Returns a json with:
        - tweet_id: UUID
        - content: str
        - created_at: datetime
        - updated_at: datetime
        - by: user: User
    """
    tweet_id = str(tweet_id)
    results = read_data("tweets")
    for tweet in results:
        if tweet["tweet_id"] == tweet_id:
            tweet["content"] = content
            tweet["updated_at"] = str(datetime.now())
            overwrite_data("tweets", results)
            return tweet
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="This tweet doesn't exist!"
        )
