from datetime import datetime
import os
from dotenv import load_dotenv

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from marshmallow import ValidationError

from db import db
from blocklist import BLOCKLIST
from resources.register import ( Register, RegisterList, RegisterRegister )
from resources.user import ( UserRegister, UserLogin, UserLogout, TokenRefresh, UserPassword, User, UserGiveAccess )
from resources.electric_meassure import ( ElectricMeassure, ElectricMeassureList )
from resources.water_meassure import ( WaterMeassure, WaterMeassureList )
from resources.meassure import (MeassureRegister, MeassuresFromRegister )
from resources.confirmation import ( Confirmation, ConfirmationByUser )
from models.user import UserModel
from schemas.user import UserSchema
from tools.enums import UserAccessLevelEnum
load_dotenv('.env')

app = Flask(__name__)

pguser = os.environ.get("PGUSER")
pghost = os.environ.get("PGHOST")
pgdatabase = os.environ.get("PGDATABASE")
pgpassword = os.environ.get("PGPASSWORD")
pgport = os.environ.get("PGPORT")
postgres_url = "postgresql://{}:{}@{}:{}/{}".format(pguser,pgpassword,pghost,pgport,pgdatabase)

app.config["SQLALCHEMY_DATABASE_URI"] = postgres_url #os.environ.get("DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config['JWT_SECRET_KEY'] = "DEVELOPMENT-SECRET-KEY"
api = Api(app)

@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400

@app.before_first_request
def create_tables():
    db.create_all()
    if not UserModel.find_by_id(1):
        user = UserSchema().load({
        "email": "admin",
        "password": "admin",
        "access_level":  UserAccessLevelEnum.ADMIN,
        "first_name": "admin",
        "last_name": "admin"
        })
        user.created_at = datetime.now()
        user.updated_at = datetime.now()
        user.save_to_db()

jwt = JWTManager(app)

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST

@app.route('/')
def home():
    return "Hello!"

api.add_resource(User, "/user")
api.add_resource(UserRegister, "/logup")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserLogout, "/logout")
api.add_resource(UserPassword, "/user/change/password")
api.add_resource(UserGiveAccess, "/user/change/access")

api.add_resource(RegisterRegister, "/register")
api.add_resource(Register, "/register/<int:id>")
api.add_resource(RegisterList, "/registers")

api.add_resource(ElectricMeassureList, "/eleMeassures")
api.add_resource(ElectricMeassure, "/eleMeassure/<int:id>")

api.add_resource(WaterMeassureList, "/watMeassures")
api.add_resource(WaterMeassure, "/watMeassure/<int:id>")

api.add_resource(MeassureRegister, "/meassure")
api.add_resource(MeassuresFromRegister,"/register/<int:registerId>/meassures")

api.add_resource(Confirmation, "/confirmation/<string:confirmation_id>")
api.add_resource(ConfirmationByUser, "/resentconfirmationemail/<string:user_email>")

if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000, debug=True, host='0.0.0.0')
    
