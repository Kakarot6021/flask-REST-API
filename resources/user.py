from db import db
from flask_smorest import abort, Blueprint
from passlib.hash import pbkdf2_sha256
from flask.views import MethodView

from flask import current_app
import redis
from rq import Queue
from tasks import send_user_registration_email  # Import the new Brevo email function

from models import UserModel
from schemas import userSchema,userRegisterSchema
import requests
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, create_refresh_token, get_jwt_identity
from blockList import BLOCKLIST

blp = Blueprint("User", "users", description="Operations on users")

@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(userRegisterSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(404, message="Username already exists..")

        user = UserModel(
            username=user_data["username"],
            email=user_data["email"],
            password=pbkdf2_sha256.hash(user_data["password"])
        )
        
        db.session.add(user)
        db.session.commit()

        # Enqueue email task using the new Brevo email function
        current_app.queue.enqueue(send_user_registration_email, user.email, user.username)

        return {"message": "User Created Successfully"}, 201

@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, userSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted."}, 200
