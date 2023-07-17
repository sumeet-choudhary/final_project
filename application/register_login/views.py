from flask import Blueprint, request, make_response, jsonify
from flask_restful import Resource
from application import api
from datetime import datetime, timedelta
import jwt
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from application.register_login.controller import add_new_user, find_user, update_verification, update_new_pass, soft_delete
import os
import bcrypt
from email.message import EmailMessage
import smtplib  # to send email


register_login_blueprint = Blueprint("register_login_blueprint", __name__)


class Register(Resource):
    def post(self):
        try:
            email = request.json.get("email")
            password = request.json.get("password").encode()
            hash_password = bcrypt.hashpw(password, bcrypt.gensalt(8))
            role = "Admin"
            verified = False
            all_values = {"email": email, "password": hash_password, "role": role, "verified": verified}

            if email in [None, ""] or password in [None, ""]:
                return make_response(jsonify({"Message": "Credential Not Found"}), 200)

            already_a_user = find_user(email)
            if already_a_user:
                return make_response(jsonify({"Message": "This User Already Exist"}), 200)

            else:
                expire_token_time = datetime.now() + timedelta(minutes=15)
                expire_epoch_time = int(expire_token_time.timestamp())
                made_payload = {"email": email, "exp": expire_epoch_time}
                made_verification_token = jwt.encode(made_payload, "sumeet", algorithm="HS256")
                # print(made_verification_token)

                email_sender = "sumeetchoudhary777@gmail.com"
                email_sender_password = os.environ.get("EMAIL_PASSWORD")
                email_receiver = email
                subject = "Dear user"
                body = f"Your verification link: " \
                       f"http://127.0.0.1:5000/verification?token={made_verification_token}"

                em = EmailMessage()
                em["FROM"] = email_sender
                em["TO"] = email_receiver
                em["SUBJECT"] = subject
                em.set_content(body)

                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(email_sender, email_sender_password)
                    smtp.sendmail(email_sender, email_receiver, em.as_string())

                if add_new_user(all_values):
                    return make_response(jsonify({"message": "Registered successfully"}))
                else:
                    return make_response(jsonify({"message": "Registered not successfully"}))

        except Exception as e:
            return make_response(jsonify({"error": str(e)}))


class Verification(Resource):
    def get(self):
        try:
            token = request.args.get("token")
            if token:
                token_decoded = jwt.decode(token, "sumeet", algorithms=["HS256"])
                email = token_decoded["email"]
                already_email_in_db = find_user(email)
                if email == already_email_in_db["email"]:
                    update_verification(email)
                return make_response(jsonify({"message": "your account is now verified"}))
        except Exception as e:
            return make_response(jsonify({"message": str(e)}))


class Login(Resource):
    def post(self):
        try:
            email = request.json.get("email", None)
            password = request.json.get("password", None).encode()
            if email:
                already_in_db = find_user(email)
                verified = already_in_db["verified"]
                if verified:
                    if already_in_db is None:
                        return make_response(jsonify({"message": "This email doesn't exists"}), 200)
                    if email == already_in_db["email"] and bcrypt.checkpw(password, already_in_db["password"]): #== already_in_db["password"]:
                        access_token = create_access_token(identity=email, expires_delta=timedelta(minutes=15))
                        refresh_token = create_refresh_token(identity=email, expires_delta=timedelta(days=1))
                        return make_response(jsonify({"message": "you have login successfully", "access_token": access_token, "refresh_token": refresh_token}), 200)
                    else:
                        return make_response(jsonify({"message": "wrong credentials"}), 500)
                else:
                    return make_response(jsonify({"message": "first verify the email"}))
        except Exception as e:
            return make_response(jsonify({'error': str(e)}))


class UpdatePassword(Resource):
    @jwt_required()
    def post(self):
        try:
            email_from_token = get_jwt_identity()
            # email_from_user = request.json.get("email", None)
            old_password = request.json.get("old_password", None).encode()
            new_password = request.json.get("new_password", None).encode()
            new_hash_password = bcrypt.hashpw(new_password, bcrypt.gensalt(8))

            already_in_db = find_user(email_from_token)
            password_in_db = already_in_db["password"]

            # if email_token == email_from_user:
            #if old_password == password_in_db:
            if bcrypt.checkpw(old_password, password_in_db):
                update_new_pass(email_from_token, new_hash_password)
                return make_response(jsonify({"message": "new password has been set"}))
            else:
                return make_response(jsonify({"message": "entered old password doesnt match"}))
            # else:
            #     return make_response(jsonify({"message": "wrong email"}))
        except Exception as e:
            return make_response(jsonify({"error": str(e)}))


class DeleteUser(Resource):
    @jwt_required()
    def post(self):
        try:
            email_from_token = get_jwt_identity()
            # password = request.json.get("password", None).encode()

            already_in_db = find_user(email_from_token)
            if already_in_db["role"] == "Admin":
                if not already_in_db:
                    return make_response(jsonify({"message": "user not found"}))
                else:
                    result = soft_delete(email_from_token)
                    if result:
                        return make_response(jsonify({"message": "user deleted successfully"}))
            else:
                return make_response(jsonify({"message": "Only Admin have the permission to delete accounts"}))
        except Exception as e:
            return make_response(jsonify({"error": str(e)}))


api.add_resource(Register, "/register")
api.add_resource(Verification, "/verification")
api.add_resource(Login, "/login")
api.add_resource(UpdatePassword, "/user/password/update")
api.add_resource(DeleteUser, "/user/delete")



