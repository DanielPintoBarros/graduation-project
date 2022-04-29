from db import db
from typing import List
from tools.enums import RegisterTypeEnum
from models.electric_meassure import ElectricMeassureModel
from models.water_meassure import WaterMeassureModel


class RegisterModel(db.Model):
    __tablename__ = 'registers'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    latitude = db.Column(db.String(20), nullable=False)
    longitude = db.Column(db.String(20), nullable=False)
    register_type = db.Column(db.Enum(RegisterTypeEnum), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("UserModel")

    water_meassures = db.relationship("WaterMeassureModel", lazy="dynamic")
    electric_meassures =  db.relationship("ElectricMeassureModel", lazy="dynamic")

    @property
    def meassures(self) -> List["WaterMeassureModel"] or List["ElectricMeassureModel"]:
        if self.is_energy:
            return self.electric_meassures
        elif self.is_water:
            return self.water_meassures
        return []

    @property
    def is_energy(self) -> bool:
        return self.register_type == RegisterTypeEnum.ENERGY

    @property
    def is_water(self) -> bool:
        return self.register_type == RegisterTypeEnum.WATER

    @classmethod
    def find_all(cls) -> List["RegisterModel"]:
        return cls.query.all()

    @classmethod
    def find_by_id(cls, _id: int) -> "RegisterModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_userId(cls, userId: int) -> "RegisterModel":
        return cls.query.filter_by(user_id=userId).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
