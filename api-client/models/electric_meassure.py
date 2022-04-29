from db import db
from typing import List


class ElectricMeassureModel(db.Model):
    __tablename__= 'electric_meassures'

    id = db.Column(db.Integer, primary_key=True)
    va = db.Column(db.Float, nullable=False)
    w = db.Column(db.Float, nullable=False)
    var = db.Column(db.Float, nullable=False)
    irms = db.Column(db.Float, nullable=False)
    vrms = db.Column(db.Float, nullable=False)
    fp = db.Column(db.Float, nullable=False)

    register_id = db.Column(db.Integer, db.ForeignKey("registers.id"))
    register = db.relationship("RegisterModel", back_populates="electric_meassures")

    @classmethod
    def find_all(cls) -> List["ElectricMeassureModel"]:
        return cls.query.all()

    @classmethod
    def find_all_by_register(cls, registerId: int) -> List["ElectricMeassureModel"]:
        return cls.query.filter_by(register_id=registerId).all()

    @classmethod
    def find_by_id(cls, _id: int) -> "ElectricMeassureModel":
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
