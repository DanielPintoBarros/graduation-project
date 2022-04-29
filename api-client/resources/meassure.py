from flask import request
from flask_restful import Resource
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
    get_jwt,
)

from models.electric_meassure import ElectricMeassureModel
from models.water_meassure import WaterMeassureModel
from models.register import RegisterModel
from models.user import UserModel
from schemas.electric_meassure import ElectricMeassureSchema
from schemas.water_meassure import WaterMeassureSchema
from tools.enums import RegisterTypeEnum, UserAccessLevelEnum
from schemas.register import RegisterSchema

from tools.helper import checkAccessAllowed

register_schema = RegisterSchema()
eleMeassure_schema = ElectricMeassureSchema()
eleMeassure_list_schema = ElectricMeassureSchema(many=True)
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
        if register.register_type == RegisterTypeEnum.ENERGY:
            meassure = eleMeassure_schema.load(meassure_json)
            meassure.register_id = register.id
        elif register.register_type == RegisterTypeEnum.WATER:
            meassure = watMeassure_schema.load(meassure_json)
            meassure.register_id = register.id
        else:
            raise Exception("Register Type not configurated")

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
        if register and register.register_type == RegisterTypeEnum.ENERGY:
            return {"register": register_schema.dump(register),
                    "meassures": eleMeassure_list_schema.dump(ElectricMeassureModel.find_all_by_register(registerId))
                }, 200
        elif register and register.register_type == RegisterTypeEnum.WATER:
            return {"register": register_schema.dump(register),
                    "meassures": watMeassure_list_schema.dump(WaterMeassureModel.find_all_by_register(registerId))
                }, 200
        else:
            raise Exception("Register Type not configurated")
