from flask import Blueprint
from app.auth.resources import RegisterResource, LoginResource, TokenRefreshResource
from app import api

auth_bp = Blueprint("auth", __name__)
api.add_resource(RegisterResource, "/auth/register")
api.add_resource(LoginResource, "/auth/login")
api.add_resource(TokenRefreshResource, "/auth/refresh")
