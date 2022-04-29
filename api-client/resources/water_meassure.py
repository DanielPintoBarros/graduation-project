from flask_restful import Resource
from flask_jwt_extended import jwt_required

from models.water_meassure import WaterMeassureModel
from schemas.water_meassure import WaterMeassureSchema
from schemas.register import RegisterSchema

from tools.enums import UserAccessLevelEnum
from tools.helper import checkAccessAllowed

register_schema = RegisterSchema()
watMeassure_schema = WaterMeassureSchema()
watMeassure_list_schema = WaterMeassureSchema(many=True)


class WaterMeassureList(Resource):
    @classmethod
    def get(cls):
        try:
            checkAccessAllowed([UserAccessLevelEnum.ADMIN, UserAccessLevelEnum.OPERATOR, UserAccessLevelEnum.VIEWER])
        except:
            return {"message": "User not allowed"}, 401

        return {"meassures": watMeassure_list_schema.dump(WaterMeassureModel.find_all())}, 200


class WaterMeassure(Resource):
    @classmethod
    def get(cls, id: int):
        try:
            checkAccessAllowed([UserAccessLevelEnum.ADMIN, UserAccessLevelEnum.OPERATOR, UserAccessLevelEnum.VIEWER])
        except:
            return {"message": "User not allowed"}, 401

        meassure = WaterMeassureModel.find_by_id(id)
        if meassure:
            return {"meassure": watMeassure_schema.dump(meassure),
                    "register": register_schema.dump(meassure.register)}, 200
        return {"message": "Meassure not found"}, 404

    @classmethod
    def delete(cls, id: int):
        try:
            checkAccessAllowed([UserAccessLevelEnum.ADMIN, UserAccessLevelEnum.OPERATOR])
        except:
            return {"message": "User not allowed"}, 401

        meassure = WaterMeassureModel.find_by_id(id)
        if meassure:
            meassure.delete_from_db()
            return {"message": "Meassure deleted from db"}, 200
        return {"message": "Measure not found"}, 404
