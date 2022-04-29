from typing import List
from flask_jwt_extended import get_jwt_identity

from models.user import UserModel
from tools.enums import UserAccessLevelEnum

def checkAccessAllowed(access_level: List):
    user_id = get_jwt_identity()
    user = UserModel.find_by_id(user_id)
    if user.access_level not in access_level:
        raise Exception("Access not allowed")
