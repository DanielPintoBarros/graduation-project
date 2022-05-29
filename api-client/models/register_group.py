from db import db
from typing import List

class RegisterGroupModel(db.Model):
    __tablename__ = "register_groups"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(50))

    registers = db.relationship("RegisterModel", lazy="dynamic", cascade="all, delete-orphan")

    @classmethod
    def find_all(cls) -> List["RegisterGroupModel"]:
        return cls.query.all()
    
    @classmethod
    def find_by_id(cls, _id: int) -> "RegisterGroupModel":
        return cls.query.filter_by(id=_id).first()
    
    @classmethod
    def find_by_name(cls, name: str) -> "RegisterGroupModel":
        return cls.query.filter_by(name=name).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()