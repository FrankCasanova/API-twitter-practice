from typing import List

from fastapi import APIRouter
from fastapi import status

from .models import LoginOut
from .models import User, Tweet
from .views import login
from .views import show_a_user
from .views import show_all_users
from .views import signup, delete_a_user, home, post, show_a_tweet, update_a_tweet, delete_a_tweet


router = APIRouter(prefix="/api/v1")


router.add_api_route(
    path="/signup",
    endpoint=signup,
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register a User",
    tags=["Users"],
    methods=["POST"],
)

router.add_api_route(
    path="/login",
    endpoint=login,
    response_model=LoginOut,  # This is the response model
    status_code=status.HTTP_200_OK,
    summary="Login a User",
    tags=["Users"],
    methods=["POST"],
)


router.add_api_route(
    path="/users",
    endpoint=show_all_users,
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="Show all User",
    tags=["Users"],
)


router.add_api_route(
    path="/users/{user_id}",
    endpoint=show_a_user,
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Show a User",
    tags=["Users"],
    methods=["GET"],
)


router.add_api_route(

    path="/users/{user_id}/delete",
    endpoint=delete_a_user,
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Delete a User",
    tags=["Users"],
    methods=["DELETE"],
)

router.add_api_route(
    path="/",
    endpoint=home,
    response_model=List[Tweet],
    status_code=status.HTTP_200_OK,
    summary="Show all Tweets",
    tags=["Tweets"],
    methods=["GET"],
)

router.add_api_route(
    path="/post",
    endpoint=post,
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary="Post a tweet",
    tags=["Tweets"],
    methods=["POST"],
)

router.add_api_route(
    path="/tweet/{tweet_id}",
    endpoint=show_a_tweet,
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Show a tweet",
    tags=["Tweets"],
    methods=["GET"],
)

router.add_api_route(
    path="/tweet/{tweet_id}/delete",
    endpoint=delete_a_tweet,
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Delete a tweet",
    tags=["Tweets"],
    methods=["DELETE"],
)


router.add_api_route(
    path="/tweet/{tweet_id}/update",
    endpoint=update_a_tweet,
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Update a tweet",
    tags=["Tweets"],
    methods=["PUT"],
)
