from ma import ma
from marshmallow import fields, post_dump
from models.meassure import MeassureModel


class MeassureSchema(ma.SQLAlchemyAutoSchema):
    @post_dump()
    def skip_null_values(self, data, **kwargs):
        return {key: value for key, value in data.items() if value is not None}

    class Meta:
        model = MeassureModel
        include_fk = True
        load_instance = True
        dump_only = ("created_at", "register_id")


class ElectricMonMeassureSchema(ma.SQLAlchemyAutoSchema):
    vrms1 = fields.Float(required=True)
    irms1 = fields.Float(required=True)
    w1 = fields.Float(required=True)
    va1 = fields.Float(required=True)
    fp1 = fields.Float(required=True)
    E1 = fields.Float(required=True)

    class Meta:
        model = MeassureModel
        include_fk = True
        load_instance = True
        dump_only = ("created_at", "register_id")
        exclude = ("vrms2","irms2","w2","va2","fp2","E2","vrms3","irms3","w3","va3","fp3","E3", "water_consume")


class ElectricBiMeassureSchema(ma.SQLAlchemyAutoSchema):
    vrms1 = fields.Float(required=True)
    irms1 = fields.Float(required=True)
    w1 = fields.Float(required=True)
    va1 = fields.Float(required=True)
    fp1 = fields.Float(required=True)
    E1 = fields.Float(required=True)
    vrms2 = fields.Float(required=True)
    irms2 = fields.Float(required=True)
    w2 = fields.Float(required=True)
    va2 = fields.Float(required=True)
    fp2 = fields.Float(required=True)
    E2 = fields.Float(required=True)

    class Meta:
        model = MeassureModel
        include_fk = True
        load_instance = True
        dump_only = ("created_at", "register_id")
        exclude = ("vrms3","irms3","w3","va3","fp3","E3", "water_consume")


class ElectricTriMeassureSchema(ma.SQLAlchemyAutoSchema):
    vrms1 = fields.Float(required=True)
    irms1 = fields.Float(required=True)
    w1 = fields.Float(required=True)
    va1 = fields.Float(required=True)
    fp1 = fields.Float(required=True)
    E1 = fields.Float(required=True)
    vrms2 = fields.Float(required=True)
    irms2 = fields.Float(required=True)
    w2 = fields.Float(required=True)
    va2 = fields.Float(required=True)
    fp2 = fields.Float(required=True)
    E2 = fields.Float(required=True)

    vrms3 = fields.Float(required=True)
    irms3 = fields.Float(required=True)
    w3 = fields.Float(required=True)
    va3 = fields.Float(required=True)
    fp3 = fields.Float(required=True)
    E3 = fields.Float(required=True)

    class Meta:
        model = MeassureModel
        include_fk = True
        load_instance = True
        dump_only = ("created_at", "register_id")
        exclude = ("water_consume",)


class WaterMeassureSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MeassureModel
        include_fk = True
        load_instance = True
        dump_only = ("created_at", "register_id")
        exclude = ("vrms1","irms1","w1","va1","fp1","E1","vrms2","irms2","w2","va2","fp2","E2","vrms3","irms3","w3","va3","fp3","E3")
