from flask_restful import Resource
from flask_jwt_extended import jwt_required

from models.electric_meassure import ElectricMeassureModel
from schemas.electric_meassure import ElectricMeassureSchema
from schemas.register import RegisterSchema

from tools.enums import UserAccessLevelEnum
from tools.helper import checkAccessAllowed

register_schema = RegisterSchema()
eleMeassure_schema = ElectricMeassureSchema()
eleMeassure_list_schema = ElectricMeassureSchema(many=True)


class ElectricMeassureList(Resource):
    @classmethod
    @jwt_required()
    def get(cls):
        try:
            checkAccessAllowed([UserAccessLevelEnum.ADMIN, UserAccessLevelEnum.OPERATOR, UserAccessLevelEnum.VIEWER])
        except:
            return {"message": "User not allowed"}, 401

        return {"meassures": eleMeassure_list_schema.dump(ElectricMeassureModel.find_all())}, 200


class ElectricMeassure(Resource):
    @classmethod
    @jwt_required()
    def get(cls, id: int):
        try:
            checkAccessAllowed([UserAccessLevelEnum.ADMIN, UserAccessLevelEnum.OPERATOR, UserAccessLevelEnum.VIEWER])
        except:
            return {"message": "User not allowed"}, 401

        meassure = ElectricMeassureModel.find_by_id(id)
        if meassure:
            return {"meassure": eleMeassure_schema.dump(meassure),
                    "register": register_schema.dump(meassure.register)}, 200
        return {"message": "Meassure not found"}, 404

    @classmethod
    @jwt_required()
    def delete(cls, id: int):
        try:
            checkAccessAllowed([UserAccessLevelEnum.ADMIN, UserAccessLevelEnum.OPERATOR])
        except:
            return {"message": "User not allowed"}, 401

        meassure = ElectricMeassureModel.find_by_id(id)
        if meassure:
            meassure.delete_from_db()
            return {"message": "Meassure deleted from db"}, 200
        return {"message": "Measure not found"}, 404
