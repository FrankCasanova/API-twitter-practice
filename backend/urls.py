from .views import login, signup, show_all_users, show_a_user
from .models import User, LoginOut

from typing import List

from fastapi import APIRouter
from fastapi import status


router = APIRouter(prefix="/api/v1")


router.add_api_route(
    path="/signup",
    endpoint=signup,
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register a User",
    tags=["Users"],
    methods=["POST"]
)

router.add_api_route(
    path="/login",
    endpoint=login,
    response_model=LoginOut,  # This is the response model
    status_code=status.HTTP_200_OK,
    summary="Login a User",
    tags=["Users"],
    methods=["POST"]
)


router.add_api_route(
    path="/users",
    endpoint=show_all_users,
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="Show all User",
    tags=["Users"]
)


router.add_api_route(
    path="/users/{user_id}",
    endpoint=show_a_user,
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Show a User",
    tags=["Users"],
    methods=["GET"]
)
