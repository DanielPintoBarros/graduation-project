from ma import ma
from models.water_meassure import WaterMeassureModel


class WaterMeassureSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = WaterMeassureModel
        include_fk = True
        load_instance = True
