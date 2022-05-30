from datetime import datetime
import os
from dotenv import load_dotenv

from flask import Flask, jsonify
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager
from marshmallow import ValidationError

from db import db
from blocklist import BLOCKLIST
from resources.alarm_definition import AlarmDefinition, AlarmDefinitionID, AlarmDefinitionRegisterID
from resources.register import ( Register, RegisterList, RegisterRegister, RegisterModbus )
from resources.register_groups import ( RegisterGroups, RegisterByRegisterGroup)
from resources.user import ( UserRegister, UserLogin, UserLogout, TokenRefresh, UserPassword, User, UserGiveAccess )
from resources.meassure import (MeassureRegister, MeassureFromRegister, MeassuresFromRegister, Meassure, MeassureList)
from resources.confirmation import ( Confirmation, ConfirmationByUser )
from models.user import UserModel
from models.confirmation import ConfirmationModel
from schemas.user import UserSchema
from tools.enums import UserAccessLevelEnum
from datetime import timedelta
load_dotenv('.env')

app = Flask(__name__)
CORS(app)

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
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=12)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
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

        confirmation = ConfirmationModel(user.id)
        confirmation.confirmed = True
        confirmation.save_to_db()


        user = UserSchema().load({
        "email": "modbus",
        "password": "modbus",
        "access_level":  UserAccessLevelEnum.OPERATOR,
        "first_name": "modbus",
        "last_name": "modbus"
        })
        user.created_at = datetime.now()
        user.updated_at = datetime.now()
        user.save_to_db()

        confirmation = ConfirmationModel(user.id)
        confirmation.confirmed = True
        confirmation.save_to_db()

jwt = JWTManager(app)

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST

@app.route('/')
def home():
    return "Hello!"

api.add_resource(User, "/user")
api.add_resource(UserRegister, "/signup")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserLogout, "/logout")
api.add_resource(UserPassword, "/user/change/password")
api.add_resource(UserGiveAccess, "/user/change/access")

api.add_resource(RegisterRegister, "/register")
api.add_resource(Register, "/register/<int:id>")
api.add_resource(RegisterList, "/registers")
api.add_resource(RegisterModbus,"/registers/modbusOn")

        
api.add_resource(RegisterGroups, "/regGroup" )
api.add_resource(RegisterByRegisterGroup, "/regGroup/<int:id>/registers" )

api.add_resource(MeassureList, "/meassures")
api.add_resource(Meassure, "/meassure/<int:id>")

api.add_resource(MeassureRegister, "/meassure")
api.add_resource(MeassureFromRegister,"/register/<int:registerId>/lastMeassure")
api.add_resource(MeassuresFromRegister,"/register/<int:registerId>/meassures")
api.add_resource(Confirmation, "/confirmation/<string:confirmation_id>")
api.add_resource(ConfirmationByUser, "/resentconfirmationemail/<string:user_email>")

api.add_resource(AlarmDefinition, '/alarmDefinitions')
api.add_resource(AlarmDefinitionID, '/alarmDefinitions/<int:id>')
api.add_resource(AlarmDefinitionRegisterID, '/register/<int:id>/alarmDefinitions')

if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000, debug=True, host='0.0.0.0')
    
