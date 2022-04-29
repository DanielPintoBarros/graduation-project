from ma import ma
from marshmallow_enum import EnumField
from models.user import UserModel
from tools.enums import UserAccessLevelEnum


class UserSchema(ma.SQLAlchemyAutoSchema):
    access_level = EnumField(UserAccessLevelEnum, by_value=True)

    class Meta:
        model = UserModel
        load_instance = True
        load_only = ("password", "access_level")
        dump_only = ("id", "created_at", "updated_at", "deleted_at")
        