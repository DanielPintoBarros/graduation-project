from ma import ma
from marshmallow import post_dump
from models.alarm_definition import AlarmDefinitionModel
from marshmallow_enum import EnumField
from tools.enums import AlarmSeverityEnum


class AlarmDefinitionSchema(ma.SQLAlchemyAutoSchema):
    severity = EnumField(AlarmSeverityEnum, by_value=True)

    @post_dump()
    def skip_null_values(self, data, **kwargs):
        return {key: value for key, value in data.items() if value is not None}

    class Meta:
        model = AlarmDefinitionModel
        include_fk = True
        load_instance = True
        dump_only = ("id",)

