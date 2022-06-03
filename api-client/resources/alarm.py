from datetime import datetime
from uuid import uuid4
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from models.alarm import AlarmModel
from models.user import UserModel
from schemas.alarm import AlarmSchema
from tools.enums import AlarmStatusEnum, UserAccessLevelEnum
from tools.helper import checkAccessAllowed
from tools.strings import gettext

alarm_schema = AlarmSchema()
alarm_list_schema = AlarmSchema(many=True)


class AlarmOpen(Resource):
    @classmethod
    @jwt_required()
    def get(cls):
        try:
            checkAccessAllowed([UserAccessLevelEnum.ADMIN, UserAccessLevelEnum.OPERATOR, UserAccessLevelEnum.VIEWER])
        except:
            return {"message": "User not allowed"}, 401

        alarms = AlarmModel.find_all_open()
        
        return {"alarms": alarm_list_schema.dump(alarms)}, 200


class AlarmCloseID(Resource):
    @classmethod
    @jwt_required()
    def post(cls, id):
        try:
            checkAccessAllowed([UserAccessLevelEnum.ADMIN, UserAccessLevelEnum.OPERATOR, UserAccessLevelEnum.VIEWER])
        except:
            return {"message": "User not allowed"}, 401

        alarm = AlarmModel.find_by_id(id)
        if alarm:
            alarm.status = AlarmStatusEnum.FINISHED
            alarm.save_to_db()
            return {"message": "Alarm closed"}, 200
        return {"message": "Alarm does not exist"}, 404
