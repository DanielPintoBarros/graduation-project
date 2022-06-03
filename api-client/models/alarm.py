from db import db
from typing import List
from tools.enums import (AlarmSeverityEnum, AlarmStatusEnum)


class AlarmModel(db.Model):
    __tablename__ = "alarms"
    
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(50))
    status = db.Column(db.Enum(AlarmStatusEnum))
    severity = db.Column(db.Enum(AlarmSeverityEnum))
    created_at = db.Column(db.TIMESTAMP)
    alarm_def_id = db.Column(db.Integer, db.ForeignKey("alarm_definitions.id"))

    alarmDef = db.relationship("AlarmDefinitionModel")

    
    @property
    def register_name(self) -> str:
        return self.alarmDef.register.name

    @property
    def register_id(self) -> str:
        return self.alarmDef.register.id

    @classmethod
    def find_by_id(cls, _id) -> "AlarmModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all_open(cls) -> List["AlarmModel"]:
        return cls.query.filter(cls.status != AlarmStatusEnum.FINISHED).order_by(cls.created_at.desc()).all()

    @classmethod
    def find_all_activated(cls) -> List["AlarmModel"]:
        return cls.query.filter_by(status=AlarmStatusEnum.ACTIVE).order_by(cls.created_at.desc()).all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()