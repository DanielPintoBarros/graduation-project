class AlarmDefinitions:
    
    def __init__(self, id, description, severity, register_id, register_type, w_thr, va_thr, irms_thr, vrms_thr, fp_thr, e_thr, water_consume_thr, water_interval):
        self.id = id
        self.description = description
        self.severity = severity
        self.register_id = register_id
        self.w_thr = w_thr
        self.va_thr = va_thr
        self.irms_thr = irms_thr
        self.vrms_thr = vrms_thr
        self.fp_thr = fp_thr
        self.e_thr = e_thr
        self.water_consume_thr = water_consume_thr
        self.water_interval = water_interval
        self.register_type = register_type

    @classmethod
    def find_all(cls, cursor):
        cursor.execute(
            'SELECT \
                ad.id, \
                ad.description, \
                ad.severity, \
                ad.register_id, \
                r.register_type, \
                ad.w_thr, \
                ad.va_thr, \
                ad.irms_thr, \
                ad.vrms_thr, \
                ad.fp_thr, \
                ad.e_thr, \
                ad.water_consume, \
                ad.water_interval \
            FROM alarm_definitions AS ad \
            JOIN registers AS r \
                ON r.id=ad.register_id \
            ORDER BY ad.register_id'
        )
        try:
            return [cls(*item) for item in cursor.fetchall()]
        except:
            return []
        
    @classmethod
    def find_by_id(cls, id, cursor):
        cursor.execute(
            'SELECT \
                ad.id, \
                ad.description, \
                ad.severity, \
                ad.register_id, \
                r.register_type, \
                ad.w_thr, \
                ad.va_thr, \
                ad.irms_thr, \
                ad.vrms_thr, \
                ad.fp_thr, \
                ad.e_thr, \
                ad.water_consume, \
                ad.water_interval \
            FROM alarm_definitions AS ad \
            JOIN registers AS r \
                ON r.id=ad.register_id \
            WHERE ad.id=%d', (id,))
        alarmDefsResponse = cursor.fetchone()
        alarmDefinition = cls(*alarmDefsResponse)

        return alarmDefinition

    def applyEnergyFilter(self, meassure):
        if self.register_type == "ENERGY1" :
            if (self.w_thr and meassure.w1 > self.w_thr or
                self.va_thr and meassure.va1 > self.va_thr or
                self.irms_thr and meassure.irms1 > self.irms_thr or
                self.vrms_thr and meassure.vrms1 > self.vrms_thr or
                self.fp_thr and meassure.fp1 < self.fp_thr or
                self.e_thr and meassure.e1 > self.e_thr):
                return True
        if self.register_type == "ENERGY2" :
           if (self.w_thr and max(meassure.w1, meassure.w2) > self.w_thr or
                self.va_thr and max(meassure.va1, meassure.va2) > self.va_thr or
                self.irms_thr and max(meassure.irms1, meassure.irms2) > self.irms_thr or
                self.vrms_thr and max(meassure.vrms1, meassure.vrms2) > self.vrms_thr or
                self.fp_thr and min(meassure.fp1, meassure.fp2) < self.fp_thr or
                self.e_thr and max(meassure.e1, meassure.e2) > self.e_thr):
                return True
        if self.register_type == "ENERGY3" :
           if  (self.w_thr and max(meassure.w1, meassure.w2, meassure.w3) > self.w_thr or
                self.va_thr and max(meassure.va1, meassure.va2, meassure.va3) > self.va_thr or
                self.irms_thr and max(meassure.irms1, meassure.irms2, meassure.irms3) > self.irms_thr or
                self.vrms_thr and max(meassure.vrms1, meassure.vrms2, meassure.vrms3) > self.vrms_thr or
                self.fp_thr and min(meassure.fp1, meassure.fp2, meassure.fp3) < self.fp_thr or
                self.e_thr and max(meassure.e1, meassure.e2, meassure.e3) > self.e_thr) :
                return True
        return False

    def applyWaterFilter(self, newMeassure, oldMeassure):
        if newMeassure.id == oldMeassure.id :
            return False
        diff = newMeassure.created_at - oldMeassure.created_at
        return (newMeassure.water_consume - oldMeassure.water_consume)/(diff.seconds/3600)  > self.water_consume_thr/ self.water_interval
