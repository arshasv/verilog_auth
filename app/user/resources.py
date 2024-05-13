from flask_restful import Resource, reqparse
from app.user.models import User
from app.user.schemas import UserSchema
from app import db

users_schema = UserSchema(many=True)
user_schema = UserSchema()


class UserResource(Resource):
    def get(self):
        users = User.query.all()
        return users_schema.dump(users)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "username", type=str, required=True, help="Username is required."
        )
        parser.add_argument("email", type=str, required=True, help="Email is required.")
        args = parser.parse_args()

        try:
            username = args["username"]
            email = args["email"]

            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                return {"message": "Username already exists"}, 409

            new_user = User(username=username, email=email)
            db.session.add(new_user)
            db.session.commit()

            return user_schema.dump(new_user), 201

        except Exception as e:
            return {"message": str(e)}
