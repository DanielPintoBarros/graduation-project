from db import db
from typing import List
from tools.enums import RegisterTypeEnum
from models.meassure import MeassureModel

class RegisterModel(db.Model):
    __tablename__ = 'registers'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    latitude = db.Column(db.String(20), nullable=False)
    longitude = db.Column(db.String(20), nullable=False)
    register_type = db.Column(db.Enum(RegisterTypeEnum), nullable=False)
    modbus_port = db.Column(db.Integer)
    register_group_id = db.Column(db.Integer, db.ForeignKey("register_groups.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    user = db.relationship("UserModel")

    meassures = db.relationship("MeassureModel", cascade="all, delete-orphan")
    
    @property
    def is_energy(self) -> bool:
        return self.register_type in [RegisterTypeEnum.ENERGY1, RegisterTypeEnum.ENERGY2, RegisterTypeEnum.ENERGY3]

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
    def find_by_group(cls, _id: int) -> List["RegisterModel"]:
        return cls.query.filter_by(register_group_id=_id).all()

    @classmethod
    def find_by_userId(cls, userId: int) -> "RegisterModel":
        return cls.query.filter_by(user_id=userId).first()

    @classmethod
    def find_modbus_on(cls) -> List["RegisterModel"]:
        return cls.query.filter(RegisterModel.modbus_port != None).all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
