from email.policy import default
from flask import request, url_for

from db import db
from models.confirmation import ConfirmationModel
from tools.enums import UserAccessLevelEnum
from emailsender import send_email


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email  = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    access_level = db.Column(db.Enum(UserAccessLevelEnum))
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    created_at = db.Column(db.TIMESTAMP, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, nullable=False)

    confirmation = db.relationship(
        "ConfirmationModel", lazy="dynamic", cascade="all, delete-orphan"
    )

    @property
    def activated(self) -> bool:
        if self.access_level == UserAccessLevelEnum.REGISTER:
            return True
        return self.most_recent_confirmation.confirmed

    @property
    def most_recent_confirmation(self) -> "ConfirmationModel":
        # ordered by expiration time (in descending order)
        return self.confirmation.order_by(db.desc(ConfirmationModel.expire_at)).first()

    @property
    def is_admin(self) -> bool:
        return self.access_level == UserAccessLevelEnum.ADMIN
    
    @property
    def is_register(self) -> bool:
        return self.access_level == UserAccessLevelEnum.REGISTER
    
    @property
    def is_operator(self) -> bool:
        return self.access_level == UserAccessLevelEnum.OPERATOR
    
    @classmethod
    def find_by_email(cls, email: str) -> 'UserModel':
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def find_by_id(cls, _id: int) -> 'UserModel':
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def send_confirmation_email(self):
        subject = "Registration Confirmation"
        link = request.url_root[:-1] + ":5000/confirmation/" + self.most_recent_confirmation.id
        html = f"<html>Please click the link to confirm your registration: <a href={link}>link</a></html>"
        send_email(self.email, subject, html)
