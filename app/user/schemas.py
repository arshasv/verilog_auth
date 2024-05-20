from marshmallow import Schema, fields, validate, validates, ValidationError
from app.user.models import User
from app import db


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    first_name = fields.String(
        required=True,
        validate=validate.Length(max=100),
        error_messages={
            "required": "First name is required.",
            "null": "First name cannot be null.",
        },
    )
    last_name = fields.String(
        required=True,
        validate=validate.Length(max=100),
        error_messages={
            "required": "Last name is required.",
            "null": "Last name cannot be null.",
        },
    )
    username = fields.String(
        required=True,
        validate=validate.Length(max=100),
        error_messages={
            "required": "Username is required.",
            "null": "Username cannot be null.",
        },
    )
    email = fields.Email(
        required=True,
        validate=validate.Length(max=100),
        error_messages={
            "required": "Email is required.",
            "null": "Email cannot be null.",
        },
    )
    password = fields.String(
        required=True,
        validate=validate.Length(max=100),
        error_messages={
            "required": "Password is required.",
            "null": "Password cannot be null.",
        },
    )
    confirm_password = fields.String(
        required=True,
        validate=validate.Length(max=100),
        error_messages={
            "required": "Confirm password is required.",
            "null": "Confirm password cannot be null.",
        },
    )

    @validates("email")
    def validate_email(self, value):
        # Check if the email already exists in the database
        if db.session.query(User.query.filter_by(email=value).exists()).scalar():
            raise ValidationError("Email already exists.")

    @validates("username")
    def validate_username(self, value):
        # Check if the username already exists in the database
        if db.session.query(User.query.filter_by(username=value).exists()).scalar():
            raise ValidationError("Username already exists.")

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
            "confirm_password",
        )
