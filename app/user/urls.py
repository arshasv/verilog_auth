from flask import Blueprint
from app.user.resources import UserResource
from app import api

user_bp = Blueprint("user", __name__)
api.add_resource(UserResource, "/users")
