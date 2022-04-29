from db import db

from tools.enums import AlarmSeverityEnum, RegisterTypeEnum


class AlarmDefinition(db.Model):
    __tablename__ = "alarm_definitions"
    
    id = db.Column(db.Integer, primary_key=True)

    register_type = db.Column(db.Enum(RegisterTypeEnum), nullable=False)

    va_m = db.Column(db.Float)
    w_m = db.Column(db.Float)
    var_m = db.Column(db.Float)
    irms_m = db.Column(db.Float)
    vrms_m = db.Column(db.Float)
    fp_m = db.Column(db.Float)

    value_m = db.Columns(db.Float)
    
    severity = db.Column(db.Enum(AlarmSeverityEnum))
    
    pass