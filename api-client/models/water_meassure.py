from db import db
from typing import List


class WaterMeassureModel(db.Model):
    __tablename__= 'water_meassures'

    id = db.Column(db.Integer, primary_key=True)

    value = db.Column(db.Float, nullable=False)
    
    register_id = db.Column(db.Integer, db.ForeignKey("registers.id"))
    register = db.relationship("RegisterModel", back_populates="water_meassures")

    @classmethod
    def find_all(cls) -> List["WaterMeassureModel"]:
        return cls.query.all()

    @classmethod
    def find_all_by_register(cls, registerId: int) -> List["WaterMeassureModel"]:
        return cls.query.filter_by(register_id=registerId).all()

    @classmethod
    def find_by_id(cls, _id: int) -> "WaterMeassureModel":
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
