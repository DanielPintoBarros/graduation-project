from datetime import datetime
from uuid import uuid4
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from models.register import RegisterModel
from models.user import UserModel
from schemas.register import RegisterSchema, RegisterModbusSchema
from tools.enums import UserAccessLevelEnum
from tools.helper import checkAccessAllowed
from tools.strings import gettext

register_schema = RegisterSchema()
register_list_schema = RegisterSchema(many=True)

register_modbus_list_schema = RegisterModbusSchema(many=True)


class RegisterRegister(Resource):
    @classmethod
    @jwt_required()
    def post(cls):
        try:
            checkAccessAllowed([UserAccessLevelEnum.ADMIN, UserAccessLevelEnum.OPERATOR])
        except:
            return {"message": "User not allowed"}, 401

        register_json = request.get_json()
        register_json["register_type"] = str(register_json["register_type"])
        print(register_json["register_group_id"])
        register = register_schema.load(register_json)
        register.save_to_db()

        user = UserModel()
        user.first_name = "Register"
        user.last_name = "{} {}".format(register.register_type.value, register.id)
        user.email = "Register{}{}".format(register.register_type.value, register.id).lower()
        user.password = str(uuid4())[:20]
        user.access_level = UserAccessLevelEnum.REGISTER
        user.created_at = datetime.now()
        user.updated_at = datetime.now()
        user.save_to_db()

        register.user_id = user.id
        register.save_to_db()
        
        return {"register": register_schema.dump(register),
                "credentials-access": {"email": user.email, "password": user.password, "message": "Save these credentials"}}, 201


class Register(Resource):
    @classmethod
    @jwt_required()
    def get(cls, id):
        try:
            checkAccessAllowed([UserAccessLevelEnum.ADMIN, UserAccessLevelEnum.OPERATOR, UserAccessLevelEnum.VIEWER])
        except:
            return {"message": "User not allowed"}, 401

        register = RegisterModel.find_by_id(id)
        if register:
            return {"register": register_schema.dump(register)}, 200
        return {"message": gettext('register_not_exists')}, 404

    @classmethod
    @jwt_required()
    def put(cls, id):
        try:
            checkAccessAllowed([UserAccessLevelEnum.ADMIN, UserAccessLevelEnum.OPERATOR])
        except:
            return {"message": "User not allowed"}, 401

        register = RegisterModel.find_by_id(id)
        
        if register:
            register_json = request.get_json()
            register_json["description"] = register_json["description"] if "description" in register_json else register.description
            register_json["latitude"] = register_json["latitude"] if "latitude" in register_json else register.latitude
            register_json["longitude"] = register_json["longitude"] if "longitude" in register_json else register.longitude
            register_json["register_type"] = str(register_json["register_type"]) if "register_type" in register_json else register.register_type
            n_register = register_schema.load(register_json)

            register.description = n_register.description
            register.latitude = n_register.latitude
            register.longitude = n_register.longitude
            register.register_type = n_register.register_type
        else:
            return {"message": gettext('register_not_exists')}, 404
        register.save_to_db()
        return {"register": register_schema.dump(register)}, 200

    @classmethod
    @jwt_required()
    def delete(cls, id):
        try:
            checkAccessAllowed([UserAccessLevelEnum.ADMIN, UserAccessLevelEnum.OPERATOR])
        except:
            return {"message": "User not allowed"}, 401

        register = RegisterModel.find_by_id(id)
        if register:
            register.delete_from_db()
            return {"message": gettext("register_deleted")}, 200
        return {"message": gettext('register_not_exists')}, 404


class RegisterList(Resource):
    @classmethod
    @jwt_required()
    def get(cls):
        try:
            checkAccessAllowed([UserAccessLevelEnum.ADMIN, UserAccessLevelEnum.OPERATOR, UserAccessLevelEnum.VIEWER])
        except:
            return {"message": "User not allowed"}, 401

        return {"registers": register_list_schema.dump(RegisterModel.find_all())}, 200


class RegisterModbus(Resource):
    @classmethod
    @jwt_required()
    def get(cls):
        try:
            checkAccessAllowed([UserAccessLevelEnum.ADMIN, UserAccessLevelEnum.OPERATOR])
        except:
            return {"message": "User not allowed"}, 401
        
        return {"registers": register_modbus_list_schema.dump(RegisterModel.find_modbus_on())}, 200