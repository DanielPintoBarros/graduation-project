from datetime import datetime
from flask import request
from flask_restful import Resource
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)

from models.meassure import MeassureModel
from models.register import RegisterModel
from schemas.meassure import MeassureSchema, ElectricMonMeassureSchema, ElectricBiMeassureSchema, ElectricTriMeassureSchema, WaterMeassureSchema
from tools.enums import RegisterTypeEnum, UserAccessLevelEnum
from schemas.register import RegisterSchema

from tools.helper import checkAccessAllowed

register_schema = RegisterSchema()
meassure_schema = MeassureSchema()
meassure_list_schema = MeassureSchema(many=True)

eleMonMeassure_schema = ElectricMonMeassureSchema()
eleMonMeassure_list_schema = ElectricMonMeassureSchema(many=True)

eleBiMeassure_schema = ElectricBiMeassureSchema()
eleBiMeassure_list_schema = ElectricBiMeassureSchema(many=True)

eleTriMeassure_schema = ElectricTriMeassureSchema()
eleTriMeassure_list_schema = ElectricTriMeassureSchema(many=True)

watMeassure_schema = WaterMeassureSchema()
watMeassure_list_schema = WaterMeassureSchema(many=True)


class MeassureRegister(Resource):
    @classmethod
    @jwt_required()
    def post(cls):
        try:
            checkAccessAllowed([UserAccessLevelEnum.REGISTER])
        except:
            return {"message": "User not allowed to store meassures"}, 401
        
        register = RegisterModel.find_by_userId(get_jwt_identity())

        meassure_json = request.get_json()
        if register.register_type == RegisterTypeEnum.ENERGY1:
            meassure = eleMonMeassure_schema.load(meassure_json)
        elif register.register_type == RegisterTypeEnum.ENERGY2:
            meassure = eleBiMeassure_schema.load(meassure_json)
        elif register.register_type == RegisterTypeEnum.ENERGY3:
            meassure = eleTriMeassure_schema.load(meassure_json)
        elif register.register_type == RegisterTypeEnum.WATER:
            meassure = watMeassure_schema.load(meassure_json)
        else:
            raise Exception("Register Type not configurated")
        meassure.created_at = datetime.now()
        meassure.register_id = register.id
        meassure.save_to_db()
        return {"message": "Meassure created"}, 201


class MeassuresFromRegister(Resource):
    @classmethod
    @jwt_required()
    def get(cls, registerId: int):
        try:
            checkAccessAllowed([UserAccessLevelEnum.ADMIN, UserAccessLevelEnum.OPERATOR, UserAccessLevelEnum.VIEWER])
        except:
            return {"message": "User not allowed"}, 401
        
        register = RegisterModel.find_by_id(registerId)
        if not register :
            return {"message": "Register does not exists"}, 404
        if register.register_type == RegisterTypeEnum.ENERGY1:
            return {"register": register_schema.dump(register),
                    "meassures": eleMonMeassure_list_schema.dump(MeassureModel.find_all_by_register(registerId))
                }, 200
        elif register.register_type == RegisterTypeEnum.ENERGY2:
            return {"register": register_schema.dump(register),
                    "meassures": eleBiMeassure_list_schema.dump(MeassureModel.find_all_by_register(registerId))
                }, 200
        elif register.register_type == RegisterTypeEnum.ENERGY3:
            return {"register": register_schema.dump(register),
                    "meassures": eleTriMeassure_list_schema.dump(MeassureModel.find_all_by_register(registerId))
                }, 200
        elif register.register_type == RegisterTypeEnum.WATER:
            return {"register": register_schema.dump(register),
                    "meassures": watMeassure_list_schema.dump(MeassureModel.find_all_by_register(registerId))
                }, 200
        else:
            raise Exception("Register Type not configurated" + register.register_type)


class MeassureFromRegister(Resource):
    @classmethod
    @jwt_required()
    def get(cls, registerId: int):
        try:
            checkAccessAllowed([UserAccessLevelEnum.ADMIN, UserAccessLevelEnum.OPERATOR, UserAccessLevelEnum.VIEWER])
        except:
            return {"message": "User not allowed"}, 401
        
        register = RegisterModel.find_by_id(registerId)
        if register and register.register_type == RegisterTypeEnum.ENERGY1:
            return {"register": register_schema.dump(register),
                    "meassure": eleMonMeassure_schema.dump(MeassureModel.last_register_meassure(registerId))
                }, 200
        elif register and register.register_type == RegisterTypeEnum.ENERGY2:
            return {"register": register_schema.dump(register),
                    "meassure": eleBiMeassure_schema.dump(MeassureModel.last_register_meassure(registerId))
                }, 200
        elif register and register.register_type == RegisterTypeEnum.ENERGY3:
            return {"register": register_schema.dump(register),
                    "meassure": eleTriMeassure_schema.dump(MeassureModel.last_register_meassure(registerId))
                }, 200
        elif register and register.register_type == RegisterTypeEnum.WATER:
            return {"register": register_schema.dump(register),
                    "meassure": watMeassure_schema.dump(MeassureModel.last_register_meassure(registerId))
                }, 200
        else:
            raise Exception("Register Type not configurated")


class MeassureList(Resource):
    @classmethod
    @jwt_required()
    def get(cls):
        try:
            checkAccessAllowed([UserAccessLevelEnum.ADMIN, UserAccessLevelEnum.OPERATOR, UserAccessLevelEnum.VIEWER])
        except:
            return {"message": "User not allowed"}, 401

        return {"meassures": meassure_list_schema.dump(MeassureModel.find_all())}, 200


class Meassure(Resource):
    @classmethod
    @jwt_required()
    def get(cls, id: int):
        try:
            checkAccessAllowed([UserAccessLevelEnum.ADMIN, UserAccessLevelEnum.OPERATOR, UserAccessLevelEnum.VIEWER])
        except:
            return {"message": "User not allowed"}, 401

        meassure = MeassureModel.find_by_id(id)
        if meassure:
            return {"meassure": meassure_schema.dump(meassure),
                    "register": register_schema.dump(meassure.register)}, 200
        return {"message": "Meassure not found"}, 404

    @classmethod
    @jwt_required()
    def delete(cls, id: int):
        try:
            checkAccessAllowed([UserAccessLevelEnum.ADMIN, UserAccessLevelEnum.OPERATOR])
        except:
            return {"message": "User not allowed"}, 401

        meassure = MeassureModel.find_by_id(id)
        if meassure:
            meassure.delete_from_db()
            return {"message": "Meassure deleted from db"}, 200
        return {"message": "Measure not found"}, 404
