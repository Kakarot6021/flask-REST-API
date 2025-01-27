from db import db
from flask_smorest import abort, Blueprint
from passlib.hash import pbkdf2_sha256
from flask.views import MethodView
from flask import current_app, jsonify
from models import UserModel
from schemas import userSchema, userRegisterSchema
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, create_refresh_token, get_jwt_identity
from blockList import BLOCKLIST
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
import os

blp = Blueprint("User", "users", description="Operations on users")

# Function to send email via Brevo
def send_email_via_brevo(to_email, username):
    api_key = os.getenv("BREVO_API_KEY")  # Load the API key from environment
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = api_key
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    # Create email object
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": to_email}],
        sender={"email": "your_email@domain.com", "name": "YourApp Name"},
        subject="Welcome to Our App!",
        html_content=f"<html><body><h1>Hi {username},</h1><p>Thank you for registering!</p></body></html>"
    )

    try:
        # Send the email via Brevo
        api_instance.send_transac_email(send_smtp_email)
        print("Email sent successfully!")
    except ApiException as e:
        print(f"Exception when calling Brevo API: {e}")

# User Logout (no changes needed here)
@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200

# User Register (now sends email directly)
@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(userRegisterSchema)
    def post(self, user_data):
        # Check if the username already exists
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(404, message="Username already exists..")

        # Create and save the new user
        user = UserModel(
            username=user_data["username"],
            email=user_data["email"],
            password=pbkdf2_sha256.hash(user_data["password"])
        )
        
        db.session.add(user)
        db.session.commit()

        # Send a welcome email directly using Brevo API
        send_email_via_brevo(user.email, user.username)

        return {"message": "User Created Successfully"}, 201

# User details and delete (no changes needed here)
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
