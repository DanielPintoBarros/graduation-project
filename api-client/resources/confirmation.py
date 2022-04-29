from flask import render_template, make_response
from flask_restful import Resource
import traceback
from time import time

from models.confirmation import ConfirmationModel
from schemas.confirmation import ConfirmationSchema
from models.user import UserModel

NOT_FOUND = "Confirmation reference not found."
EXPIRED = "The link has expired."
ALREADY_CONFIRMED = "Registration has already been confirmed."
RESEND_FAIL = "Internal server error. Failed to resend confirmation email."
RESEND_SUCCESSFUL = "E-mail confirmation successfully re-sent."

confirmation_schema = ConfirmationSchema()


class Confirmation(Resource):
    @classmethod
    def get(cls, confirmation_id: str):
        confirmation = ConfirmationModel.find_by_id(confirmation_id)
        if not confirmation:
            return {"message": NOT_FOUND}, 404

        if confirmation.expired:
            return {"message": EXPIRED}, 400

        if confirmation.confirmed:
            return {"message": ALREADY_CONFIRMED}, 400

        confirmation.confirmed = True
        confirmation.save_to_db()

        return {"message": "Confirmation completed!"}, 200


class ConfirmationByUser(Resource):
    @classmethod
    def post(cls, user_email):
        user = UserModel.find_by_email(user_email)
        if not user:
            return {"message": "Usuario não encontrado"}, 404

        try:
            confirmation = user.most_recent_confirmation
            if confirmation:
                if confirmation.confirmed:
                    return {"message": ALREADY_CONFIRMED}, 400
                confirmation.force_to_expire()

            new_confirmation = ConfirmationModel(user.id)
            new_confirmation.save_to_db()
            user.send_confirmation_email()
            return {"message": RESEND_SUCCESSFUL}, 201
        except:
            traceback.print_exc()
            return {"message": RESEND_FAIL}, 500