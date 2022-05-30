from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models.alarm_definition import AlarmDefinitionModel
from models.register import RegisterModel
import sys

from tools.helper import checkAccessAllowed
from tools.enums import UserAccessLevelEnum

from schemas.alarm_definition import  AlarmDefinitionSchema

alarmDef_schema = AlarmDefinitionSchema()
alarmDef_list_schema = AlarmDefinitionSchema(many=True)



class AlarmDefinition(Resource):
    @classmethod
    @jwt_required()
    def get(cls):
        try:
            checkAccessAllowed([UserAccessLevelEnum.VIEWER, UserAccessLevelEnum.OPERATOR, UserAccessLevelEnum.ADMIN])
        except:
            return {"message": "User not allowed"}, 401
        return {"alarmDef": alarmDef_list_schema.dump(AlarmDefinitionModel.find_all())}, 200
    
    @classmethod
    @jwt_required()
    def post(cls):
        try:
            checkAccessAllowed([UserAccessLevelEnum.OPERATOR, UserAccessLevelEnum.ADMIN])
        except:
            return {"message": "User not allowed"}, 401
        
        alarmDef_json = request.get_json()
        alarmDef = alarmDef_schema.load(alarmDef_json)
        alarmDef.save_to_db()    
        
        return {"message": "Alarm definition created"}, 201


class AlarmDefinitionID(Resource):
    @classmethod
    @jwt_required()
    def get(cls,id):
        try:
            checkAccessAllowed([UserAccessLevelEnum.VIEWER, UserAccessLevelEnum.OPERATOR, UserAccessLevelEnum.ADMIN])
        except:
            return {"message": "User not allowed"}, 401
        
        alarmDef = AlarmDefinitionModel.find_by_id(id)
        if alarmDef:
            return {"alarmDef": alarmDef_schema.dump(alarmDef)}, 200

        return {"message": "Alarm definition does not exist"}, 404

    @classmethod
    @jwt_required()
    def delete(cls, id):
        try:
            checkAccessAllowed([UserAccessLevelEnum.OPERATOR, UserAccessLevelEnum.ADMIN])
        except:
            return {"message": "User not allowed"}, 401
        alarmDef = AlarmDefinitionModel.find_by_id(id)

        if alarmDef:
            alarmDef.delete_from_db()
        else:
            return {"message": "Alarm definition does not exist"}, 404
        return {"message": "Alarm definition deleted"}, 200

class AlarmDefinitionRegisterID(Resource):
    @classmethod
    @jwt_required()
    def get(cls,id):
        try:
            checkAccessAllowed([UserAccessLevelEnum.VIEWER, UserAccessLevelEnum.OPERATOR, UserAccessLevelEnum.ADMIN])
        except:
            return {"message": "User not allowed"}, 401
        register = RegisterModel.find_by_id(id)
        if register:
            alarmDefs = AlarmDefinitionModel.fing_by_register_id(id)
            return {"alarmDef": alarmDef_list_schema.dump(alarmDefs)}, 200

        return {"message": "Register does not exist"}, 404
