from ma import ma
from models.register_group import RegisterGroupModel


class RegisterGroupSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RegisterGroupModel
        load_instance = True
        include_fk = True