from ma import ma
from marshmallow import post_dump
from marshmallow import fields
from models.alarm import AlarmModel
from marshmallow_enum import EnumField
from tools.enums import AlarmSeverityEnum, AlarmStatusEnum

from schemas.alarm_definition import AlarmDefinitionSchema


from ma import ma



class AlarmSchema(ma.SQLAlchemyAutoSchema):
    severity = EnumField(AlarmSeverityEnum, by_value=True)
    status = EnumField(AlarmStatusEnum, by_value=True)
    register_id = fields.Integer(required=True)
    register_name = fields.Str(required=True)

    #alarmDefinition = fields.Nested(AlarmDefinitionSchema)

    @post_dump()
    def skip_null_values(self, data, **kwargs):
        return {key: value for key, value in data.items() if value is not None}

    class Meta:
        model = AlarmModel
        include_fk = True
        load_instance = True
        dump_only = ("id", "register_id", "register_name")

