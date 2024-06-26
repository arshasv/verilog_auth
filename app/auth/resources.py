import json
from flask_restful import Resource, reqparse
from marshmallow import ValidationError
from flask import request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)
from app.user.models import User
from app.user.schemas import UserSchema
from app import db

users_schema = UserSchema(many=True)
user_schema = UserSchema()


class RegisterResource(Resource):

    def post(self):
        json_data = request.get_json()
        # Load data into User schema for validation
        try:
            data = user_schema.load(json_data)

        except ValidationError as err:
            print(err)
            return dict({"message": err.messages}), 400
        # add new user to the db

        password = data["password"]
        confirm_password = data["confirm_password"]

        # Check passwords match (already done in schema but let's confirm)
        if password != confirm_password:
            return {"error": "Passwords do not match"}, 400

        try:
            new_user = User(**data)
            db.session.add(new_user)
            db.session.commit()

            # when authenticated, return a fresh access token and a refresh token
            access_token = create_access_token(identity=new_user.id, fresh=True)
            refresh_token = create_refresh_token(new_user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        except Exception as e:
            return {"message": str(e)}


class LoginResource(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "username", type=str, required=True, help="Username is required."
        )
        parser.add_argument(
            "password", type=str, required=True, help="Password is required."
        )
        args = parser.parse_args()
        username = args["username"]
        password = args["password"]
        # read from database to find the user and then check the password
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            # when authenticated, return a fresh access token and a refresh token
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        return {"message": "Invalid Credentials!"}, 401


class TokenRefreshResource(Resource):
    @jwt_required(refresh=True)
    def post(self):
        # retrive the user's identity from the refresh token using a Flask-JWT-Extended built-in method
        current_user = get_jwt_identity()
        # return a non-fresh token for the user
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200
