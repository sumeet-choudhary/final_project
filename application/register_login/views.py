from flask import Flask, Blueprint, request, make_response, jsonify
from flask_restful import Api, Resource
from application import api
from datetime import datetime, timedelta
import jwt
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required
from application.register_login.controller2 import (
    add_new_user,
    find_user,
    update_verify,
    update_new_pass,
    delete_user,
)
import os
from email.message import EmailMessage
import smtplib  # to send email


register_login_blueprint = Blueprint("register_login_blueprint", __name__)


class Register(Resource):
    def post(self):
        try:
            email = request.json.get("email")
            password = request.json.get("password")
            role = "Admin"
            verified = False
            all_values = {
                "email": email,
                "password": password,
                "role": role,
                "verified": verified,
            }

            if email in [None, ""] or password in [None, ""]:
                return make_response(jsonify({"Message": "Credential Not Found"}), 200)

            already_a_user = find_user(email)
            if already_a_user:
                return make_response(
                    jsonify({"Message": "This User Already Exist"}), 200
                )

            else:
                expire_token_time = datetime.now() + timedelta(minutes=15)
                expire_epoch_time = int(expire_token_time.timestamp())
                made_payload = {"email": email, "exp": expire_epoch_time}
                made_verification_token = jwt.encode(
                    made_payload, "sumeet", algorithm="HS256"
                )

                email_sender = "sumeetchoudhary777@gmail.com"
                email_sender_password = os.environ.get("EMAIL_PASSWORD")
                email_receiver = email
                subject = "NEW MAIL"
                body = made_verification_token

                em = EmailMessage()
                em["FROM"] = email_sender
                em["TO"] = email_receiver
                em["SUBJECT"] = subject
                em.set_content(body)

                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                    smtp.login(email_sender, email_sender_password)
                    smtp.sendmail(email_sender, email_receiver, em.as_string())

                if add_new_user(all_values):
                    return make_response(
                        jsonify({"message": "Registered successfully"})
                    )
                else:
                    return make_response(
                        jsonify({"message": "Registered not successfully"})
                    )

        except Exception as e:
            return make_response(jsonify({"error": str(e)}))


class Verification(Resource):
    def post(self):
        try:
            token = request.args.get("token")
            if token:
                token_decoded = jwt.decode(token, "sumeet", algorithm=["HS256"])
                email = token_decoded["email"]
                already_email_in_db = find_user(email)
                if email == already_email_in_db["email"]:
                    update_verify(email)
                return make_response(
                    jsonify({"message": "your account is now verified"})
                )
        except Exception as e:
            return make_response(jsonify({"message": str(e)}))


class Login(Resource):
    def post(self):
        try:
            email = request.json.get("email", None)
            password = request.json.get("password", None)
            if email:
                already_in_db = find_user(email)
                print(already_in_db)
                if (
                    email == already_in_db["email"]
                    and password == already_in_db["password"]
                ):
                    return make_response(
                        jsonify({"message": "you have login successfully"})
                    )
                else:
                    return make_response(jsonify({"message": "wrong credentials"}))
        except Exception as e:
            return make_response(jsonify({"error": str(e)}))


class UpdatePassword(Resource):
    @jwt_required()
    def post(self):
        try:
            email = request.json.get("email", None)
            old_password = request.json.get("old_passowrd", None)
            new_password = request.json.get("new_password", None)

            already_in_db = find_user(email)
            email_in_db = already_in_db["email"]
            password_in_db = already_in_db["password"]

            if old_password == password_in_db:
                update_new_pass(email, new_password)
                return make_response(jsonify({"message": "new password has been set"}))
            else:
                return make_response(
                    jsonify({"message": "entered old password doesnt match"})
                )
        except Exception as e:
            return make_response(jsonify({"error": str(e)}))


class DeleteUser(Resource):
    @jwt_required
    def post(self):
        try:
            email = request.json.get("email", None)
            password = request.json.get("passowrd", None)

            already_in_db = find_user(email)
            if not already_in_db:
                return make_response(jsonify({"message": "user not found"}))
            else:
                result = delete_user(email)
                if result:
                    return make_response(
                        jsonify({"message": "User deleted successfully"})
                    )
        except Exception as e:
            return make_response(jsonify({"error": str(e)}))


api.add_resource(Register, "/register")
api.add_resource(Verification, "/verification")
api.add_resource(Login, "/login")
api.add_resource(UpdatePassword, "/updatepassword")
api.add_resource(DeleteUser, "/deleteuser")
