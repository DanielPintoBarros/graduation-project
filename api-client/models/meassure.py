from db import db
from typing import List


class MeassureModel(db.Model):
    __tablename__= 'meassures'

    id = db.Column(db.Integer, primary_key=True)
    vrms1 = db.Column(db.Float)
    irms1 = db.Column(db.Float)
    w1 = db.Column(db.Float)
    va1 = db.Column(db.Float)
    fp1 = db.Column(db.Float)
    E1 = db.Column(db.Float)

    vrms2 = db.Column(db.Float)
    irms2 = db.Column(db.Float)
    w2 = db.Column(db.Float)
    va2 = db.Column(db.Float)
    fp2 = db.Column(db.Float)
    E2 = db.Column(db.Float)

    vrms3 = db.Column(db.Float)
    irms3 = db.Column(db.Float)
    w3 = db.Column(db.Float)
    va3 = db.Column(db.Float)
    fp3 = db.Column(db.Float)
    E3 = db.Column(db.Float)

    water_consume = db.Column(db.Float)

    created_at = db.Column(db.Date(), nullable=False)

    register_id = db.Column(db.Integer, db.ForeignKey("registers.id"), nullable=False)

    @classmethod
    def find_all(cls) -> List["MeassureModel"]:
        return cls.query.all()

    @classmethod
    def find_all_by_register(cls, registerId: int) -> List["MeassureModel"]:
        return cls.query.filter_by(register_id=registerId).all()

    @classmethod
    def find_by_id(cls, _id: int) -> "MeassureModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def last_register_meassure(cls, _id: int) -> "MeassureModel":
        return cls.query.filter_by(register_id=_id).order_by(cls.id.desc()).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
