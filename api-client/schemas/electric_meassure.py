from ma import ma
from models.electric_meassure import ElectricMeassureModel


class ElectricMeassureSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ElectricMeassureModel
        include_fk = True
        load_instance = True
