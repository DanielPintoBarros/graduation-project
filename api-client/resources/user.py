from datetime import datetime
from flask import request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    get_jwt,
)
from flask_restful import Resource
from models.register import RegisterModel

from models.user import UserModel
from models.confirmation import ConfirmationModel
from schemas.user import UserSchema
from tools.strings import gettext
from tools.enums import UserAccessLevelEnum
from tools.helper import checkAccessAllowed
from blocklist import BLOCKLIST

user_schema = UserSchema()


class User(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        user_json = request.get_json()

        if "first_name" in user_json:
            user.first_name = user_json["first_name"]
        if "last_name" in user_json:
            user.last_name = user_json["last_name"]
        if "email" in user_json:
            user.email = user_json["email"]

            user.most_recent_confirmation.confirmed = False
            user.most_recent_confirmation.force_to_expire()

            confirmation = ConfirmationModel(user.id)
            confirmation.save_to_db()

        user.updated_at = datetime.now()
        user.save_to_db()

        if "email" in user_json:
            user.send_confirmation_email()
        return {"user": user}, 200


    @classmethod
    @jwt_required
    def delete(cls):
        jti = get_jwt()["jti"]
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        if (user.is_register):
            register = RegisterModel.find_by_userId(user_id)
            register.delete_from_db()
        user.delete_from_db()

        BLOCKLIST.add(jti)
        return {"message": "User deleted"}, 200


class UserPassword(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        json = request.get_json()
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)

        if "password" in json:
            user.password = json["password"]

            jti = get_jwt()["jti"]
            BLOCKLIST.add(jti)

            return {"message": "Password changed!"}, 200
        return {"message": "Attribute 'password' is required"}, 400


class UserGiveAccess(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        try:
            checkAccessAllowed([UserAccessLevelEnum.ADMIN])
        except:
            return {"message": "User not allowed"}, 401

        json = request.get_json()
        if "email" not in json or "access_level" not in json:
            return {"message": "fields 'email' and 'access_level' are required"}, 400
        if json["access_level"] not in UserAccessLevelEnum._value2member_map_:
            return {"message": "'access_level' should be one of the followings 'ADMIN', 'VIEWER', 'OPERATOR'"}
        
        user = UserModel.find_by_email(json["email"])
        user.access_level = UserAccessLevelEnum(json["access_level"])
        user.save_to_db()

        return {"message": "User {}, is now a {}".format(user.email, user.access_level)}, 200


class UserRegister(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        user = user_schema.load(user_json)
        user.email = user.email.lower()

        if UserModel.find_by_email(user.email):
            return {"message": gettext('user_email_exists').format(user.email)}, 400
        user.access_level = UserAccessLevelEnum.VIEWER
        user.created_at = datetime.now()
        user.updated_at = datetime.now()

        try:
            user.save_to_db()

            confirmation = ConfirmationModel(user.id)
            confirmation.save_to_db()

            print("prepare to send email")
            user.send_confirmation_email()
            return {"messsage": "User created! We send you a email to confirm the registration.",
                    "user": user_schema.dump(user)}, 201
        except Exception as e:
            user.delete_from_db()
            return {"message": "Failed to create a user"}, 500


class UserLogin(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        user_data = user_schema.load(user_json, partial=("username", "access_level", "first_name", "last_name"))

        user = UserModel.find_by_email(user_data.email.lower())

        if user and user.password == user_data.password:
            if user.activated:
                access_token = create_access_token(user.id, fresh=True)
                refresh_token = create_refresh_token(user.id)
                return {"access_token": access_token, "refresh_token": refresh_token}, 200
            return {"message": "You must activate your account. Check your email"}, 401

        return {"message": gettext("user_invalid_credentials")}, 401


class UserLogout(Resource):
    @classmethod
    @jwt_required()
    def post(cls):
        jti = get_jwt()["jti"]
        user_id = get_jwt_identity()
        BLOCKLIST.add(jti)
        return {"message": gettext("user_logged_out").format(user_id)}, 200


class TokenRefresh(Resource):
    @classmethod
    @jwt_required(refresh=True)
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200
