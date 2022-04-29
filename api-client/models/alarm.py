from db import db
from typing import List
from tools.enums import (AlarmSeverityEnum, AlarmStatusEnum)


class AlarmModel(db.Model):
    __tablename__ = "alarms"
    
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(50))
    status = db.Column(db.Enum(AlarmStatusEnum))
    severity = db.Column(db.Enum(AlarmSeverityEnum))
    created_at = db.Column(db.DateTime)
    alarm_def_id = db.Column(db.Integer, db.ForeignKey("alarm_definitions.id"))

    
    @classmethod
    def find_all_activated(cls) -> List["AlarmModel"]:
        return cls.query.filter_by(status=AlarmStatusEnum.ACTIVE).all()