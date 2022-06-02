from datetime import datetime


class Meassures:

    def __init__(self, id, register_id, created_at, vrms1, irms1, w1, va1, fp1, e1, vrms2, irms2, w2, va2, fp2, e2, vrms3, irms3, w3, va3, fp3, e3, water_consume) -> None:
        self.id = id
        self.register_id = register_id
        self.created_at = created_at
        self.vrms1 = vrms1
        self.irms1 = irms1
        self.w1 = w1
        self.va1 = va1
        self.fp1 = fp1
        self.e1 = e1
        self.vrms2 = vrms2
        self.irms2 = irms2
        self.w2 = w2
        self.va2 = va2
        self.fp2 = fp2
        self.e2 = e2
        self.vrms3 = vrms3
        self.irms3 = irms3
        self.w3 = w3
        self.va3 = va3
        self.fp3 = fp3
        self.e3 = e3
        self.water_consume = water_consume
    
    @classmethod
    def findMWByRegId(cls, registerID, initDate, cursor):

        cursor.execute(
            'SELECT \
                id, \
                register_id, \
                created_at, \
                vrms1, \
                irms1, \
                w1, \
                va1, \
                fp1, \
                e1, \
                vrms2, \
                irms2, \
                w2, \
                va2, \
                fp2, \
                e2, \
                vrms3, \
                irms3, \
                w3, \
                va3, \
                fp3, \
                e3, \
                water_consume \
            FROM meassures \
            WHERE \
                register_id = %s AND \
                created_at >= %s \
            ORDER BY created_at DESC \
            LIMIT 1', (registerID, initDate)
        )
        item = cursor.fetchone()
        if item:
            return cls(*item)
        return None

    @classmethod
    def findMWByInterval(cls, registerID, initDate, cursor):
        cursor.execute(
            'SELECT \
                id, \
                register_id, \
                created_at, \
                vrms1, \
                irms1, \
                w1, \
                va1, \
                fp1, \
                e1, \
                vrms2, \
                irms2, \
                w2, \
                va2, \
                fp2, \
                e2, \
                vrms3, \
                irms3, \
                w3, \
                va3, \
                fp3, \
                e3, \
                water_consume \
            FROM meassures \
            WHERE \
                register_id = %s AND \
                created_at >= %s \
            ORDER BY created_at ASC \
            LIMIT 1', (registerID,initDate)
        )
        item = cursor.fetchone()
        if item:
            return cls(*item)
        return None

    @classmethod
    def findMEByRegId(cls, registerIDs, cursor, initDate):
        registerIDFilter = "register_id in ({})".format(",".join(["%s" for id in registerIDs]))

        cursor.execute(
            'SELECT\
                id, \
                register_id, \
                created_at, \
                vrms1, \
                irms1, \
                w1, \
                va1, \
                fp1, \
                e1, \
                vrms2, \
                irms2, \
                w2, \
                va2, \
                fp2, \
                e2, \
                vrms3, \
                irms3, \
                w3, \
                va3, \
                fp3, \
                e3, \
                water_consume \
            FROM meassures \
            WHERE {} AND\
                created_at>=%s \
            ORDER BY register_id'.format(registerIDFilter), (*registerIDs,initDate)
        )

        meassures = [cls(*item) for item in cursor.fetchall()]
        return meassures