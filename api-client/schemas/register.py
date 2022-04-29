from ma import ma
from marshmallow_enum import EnumField
from models.register import RegisterModel
from tools.enums import RegisterTypeEnum


class RegisterSchema(ma.SQLAlchemyAutoSchema):
    register_type = EnumField(RegisterTypeEnum, by_value=True)
    
    class Meta:
        model = RegisterModel
        load_instance = True
        dump_only = ("id", "user_id")
