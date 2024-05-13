from app import ma
from app.user.models import User


class UserSchema(ma.Schema):
    class Meta:
        model = User
        fields = ("username", "email")
