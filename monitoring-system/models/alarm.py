

class Alarm:
    def __init__(self, id, description, status, severity, created_at, alarm_def_id):
        self.id = id
        self.description = description
        self.status = status
        self.severity = severity
        self.created_at = created_at
        self.alarm_def_id = alarm_def_id

    @classmethod
    def findAll(cls,cursor, alarmDefinitions):
        alarmDefIDFilter = "alarm_def_id in ({})".format(",".join([str(ad.id) for ad in alarmDefinitions]))
        print(alarmDefIDFilter)
        cursor.execute(
            'SELECT \
                id, \
                description, \
                status, \
                severity, \
                created_at, \
                alarm_def_id \
            FROM \
                alarms \
            WHERE \
                status=%s AND \
                {}  '.format(alarmDefIDFilter), ("ACTIVE",)
        )
        try:
            items = cursor.fetchall()
            alarms = {item[5]: cls(*item) for item in items}
        except:
            alarms = {}
        alarmDef_alarm = [{"definition": alarmDef, "alarm": alarms.get(alarmDef.id)} for alarmDef in alarmDefinitions]


        return alarmDef_alarm
    
    def resolveAlarm(self, cursor):
        cursor.execute(
            'UPDATE alarms \
            SET \
                status=%s \
            WHERE \
                id=%s', ("RESOLVED",self.id)
        )
        
    def create_in_db(self, cursor):
        cursor.execute(
            'INSERT INTO alarms \
                (description,status,severity,created_at,alarm_def_id) \
            VALUES \
                (%s,%s,%s,%s,%s) \
            RETURNING id', (self.description, self.status, self.severity, self.created_at, self.alarm_def_id)
        )

        self.id = cursor.fetchone()[0]




