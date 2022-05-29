
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models.register_group import RegisterGroupModel
from models.register import RegisterModel

from tools.helper import checkAccessAllowed
from tools.enums import UserAccessLevelEnum

from schemas.register_groups import  RegisterGroupSchema
from schemas.register import  RegisterSchema

groups_schema = RegisterGroupSchema()
groups_list_schema = RegisterGroupSchema(many=True)
register_list_schema = RegisterSchema(many=True)


class RegisterGroups(Resource):
    @classmethod
    @jwt_required()
    def get(cls):
        try:
            checkAccessAllowed([UserAccessLevelEnum.VIEWER, UserAccessLevelEnum.OPERATOR, UserAccessLevelEnum.ADMIN])
        except:
            return {"message": "User not allowed"}, 401
        return {"groups": groups_list_schema.dump(RegisterGroupModel.find_all())}, 200
    
    @classmethod
    @jwt_required()
    def post(cls):
        try:
            checkAccessAllowed([UserAccessLevelEnum.VIEWER, UserAccessLevelEnum.OPERATOR, UserAccessLevelEnum.ADMIN])
        except:
            return {"message": "User not allowed"}, 401
        
        group_json = request.get_json()
        group = groups_schema.load(group_json)
        group.save_to_db()    
        
        return {"message": "Group created"}, 201
    
    @classmethod
    @jwt_required()
    def put(cls):
        try:
            checkAccessAllowed([UserAccessLevelEnum.OPERATOR, UserAccessLevelEnum.ADMIN])
        except:
            return {"message": "User not allowed"}, 401
        group_json = request.get_json()
        group = RegisterGroupModel.find_by_id(group_json["id"])

        if group:
            
            group_json["name"] = group_json["name"] if "name" in group_json else group.name
            group_json["description"] = group_json["description"] if "description" in group_json else group.description
            del group_json["id"]
            n_group = groups_schema.load(group_json)

            group.name = n_group.name
            group.description = n_group.description
            
        else:
            return {"message": "Register Group does not exist"}, 404
        group.save_to_db()
        return {"group": groups_schema.dump(group)}, 200

    @classmethod
    @jwt_required()
    def delete(cls):
        try:
            checkAccessAllowed([UserAccessLevelEnum.OPERATOR, UserAccessLevelEnum.ADMIN])
        except:
            return {"message": "User not allowed"}, 401
        group_json = request.get_json()
        group = RegisterGroupModel.find_by_id(group_json["id"])

        if group:
            group.delete_from_db()
        else:
            return {"message": "Register Group does not exist"}, 404
        return {"message": "Register Group deleted"}, 200

class RegisterByRegisterGroup(Resource):
    @classmethod
    @jwt_required()
    def get(cls, id):
        try:
            checkAccessAllowed([UserAccessLevelEnum.VIEWER, UserAccessLevelEnum.OPERATOR, UserAccessLevelEnum.ADMIN])
        except:
            return {"message": "User not allowed"}, 401

        return {"registers": register_list_schema.dump(RegisterModel.find_by_group(id))}, 200
    