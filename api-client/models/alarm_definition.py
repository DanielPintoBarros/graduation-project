from db import db
from typing import List

from tools.enums import AlarmSeverityEnum


class AlarmDefinitionModel(db.Model):
    __tablename__ = "alarm_definitions"
    
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    severity = db.Column(db.Enum(AlarmSeverityEnum), nullable=False)
    register_id = db.Column(db.Integer, db.ForeignKey("registers.id"), nullable=False)

    w_thr = db.Column(db.Float)
    va_thr = db.Column(db.Float)
    irms_thr = db.Column(db.Float)
    vrms_thr = db.Column(db.Float)
    fp_thr = db.Column(db.Float)
    e_thr = db.Column(db.Float)

    water_consume = db.Column(db.Float)
    water_interval = db.Column(db.Integer)

    
    @classmethod
    def find_all(cls) -> List["AlarmDefinitionModel"]:
        return cls.query.all()

    @classmethod
    def find_by_id(cls, _id: int) -> "AlarmDefinitionModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def fing_by_register_id(cls, _id: int) -> List["AlarmDefinitionModel"]:
        return cls.query.filter_by(register_id=_id).all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
