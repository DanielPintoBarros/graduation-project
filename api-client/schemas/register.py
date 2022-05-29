from ma import ma
from marshmallow import fields
from marshmallow_enum import EnumField
from models.register import RegisterModel
from schemas.user import UserModbusSchema
from tools.enums import RegisterTypeEnum


class RegisterSchema(ma.SQLAlchemyAutoSchema):
    register_type = EnumField(RegisterTypeEnum, by_value=True)
    
    class Meta:
        model = RegisterModel
        include_fk = True
        load_instance = True
        dump_only = ("id", "user_id")


class RegisterModbusSchema(ma.SQLAlchemyAutoSchema):
    register_type = EnumField(RegisterTypeEnum, by_value=True)
    user = fields.Nested(UserModbusSchema)
    
    class Meta:
            model = RegisterModel
            load_instance = True
            load_only = ("latitude", "longitude", "description")
            dump_only = ("id", "user_id", "user")
