from datetime import datetime, timedelta
import psycopg2
from models.alarm_definitions import AlarmDefinitions
from models.meassures import Meassures
from models.alarm import Alarm
import os
import time

def createAndInitiateVarTable(conn, last_eleCheck, last_watCheck):
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS monitoring_system_var ( \
            var varchar(20) UNIQUE, \
            value timestamp \
        );")
    conn.commit()

    cursor.execute(
        "SELECT value \
        FROM monitoring_system_var \
        WHERE \
            var = %s OR var = %s", ("last_elecheck","last_watcheck")
    )
    var = cursor.fetchall()
    try:
        if var:
            cursor.execute(
                "UPDATE monitoring_system_var \
                SET \
                    value=%s \
                WHERE \
                    var=%s \
            ",(last_eleCheck,"last_elecheck"))

            cursor.execute(
                "UPDATE monitoring_system_var \
                SET \
                    value=%s \
                WHERE \
                    var=%s \
            ",(last_watCheck,"last_watcheck"))
            conn.commit()
        else:
            cursor.execute(
            "INSERT INTO monitoring_system_var \
                (var, value) \
            VALUES \
                (%s,%s), \
                (%s,%s)"
        , ("last_elecheck", last_eleCheck, "last_watcheck", last_watCheck))
            conn.commit()

    except (Exception, psycopg2.DatabaseError):
        return False
    return True

def runAlarmCheckAndCreationRoutine(conn):
    def getLastCheck(cursor):
        cursor.execute(
            "SELECT value \
            FROM monitoring_system_var \
            WHERE \
                var = %s ", ("last_elecheck",)
        )
        last_eleCheck = cursor.fetchone()
        cursor.execute(
            "SELECT value \
            FROM monitoring_system_var \
            WHERE \
                var = %s ", ("last_watcheck",)
        )
        last_watCheck = cursor.fetchone()
        
        return (last_eleCheck, last_watCheck)

    (last_eleCheck, last_watCheck) = getLastCheck(conn.cursor())
    alarmDefinitions = AlarmDefinitions.find_all(conn.cursor())
    if len(alarmDefinitions) == 0:
        return
    alarmsDef_alarms = Alarm.findAll(conn.cursor(), alarmDefinitions)
    energyRegIDs = list({ad.register_id for ad in alarmDefinitions if "ENERGY" in ad.register_type})
    waterRegIDs = list({ad.register_id for ad in alarmDefinitions if "WATER" in ad.register_type})

    eleMeassures = Meassures.findMEByRegId(energyRegIDs, conn.cursor(), last_eleCheck)
    last_eleCheck  = datetime.utcnow()
    waterMeassures = {regId: Meassures.findMWByRegId(regId,last_watCheck ,conn.cursor()) for regId in waterRegIDs}
    last_watCheck = datetime.utcnow()

        
    alarmsDefMapByRegId = {reg: [] for reg in [*energyRegIDs,*waterRegIDs]}
    for alarm in alarmsDef_alarms :
        alarmsDefMapByRegId.get(alarm.get("definition").register_id).append(alarm)

    for m in eleMeassures:
        hadChange = False
        for alarmDefAlarm in alarmsDefMapByRegId.get(m.register_id):
            alarmDef = alarmDefAlarm.get("definition")
            alarm = alarmDefAlarm.get("alarm")
            if alarmDef.applyEnergyFilter(m):
                if alarm is None:
                    alarm = Alarm(id=None, description=alarmDef.description, status="ACTIVE", severity=alarmDef.severity, created_at=datetime.utcnow(), alarm_def_id=alarmDef.id)
                    alarm.create_in_db(conn.cursor())
                    alarmDefAlarm.update({"alarm": alarm})
                    hadChange = True
            else:
                if alarm:
                    alarm.status = "RESOLVED"
                    alarm.resolveAlarm(conn.cursor())
                    alarmDefAlarm.update({"alarm": None})
                    hadChange = True
        if hadChange:
            conn.commit()

    for regId in waterRegIDs:
        m0 = waterMeassures.get(regId)
        if m0:
            for alarmDefAlarm in alarmsDefMapByRegId.get(regId):
                alarmDef = alarmDefAlarm.get("definition")
                alarm = alarmDefAlarm.get("alarm")
                
                interval = m0.created_at - timedelta(hours=alarmDef.water_interval)
                m1 = Meassures.findMWByInterval(regId, interval, conn.cursor())
                if alarmDef.applyWaterFilter(m0, m1):
                    if alarm is None:
                        alarm = Alarm(id=None, description=alarmDef.description, status="ACTIVE", severity=alarmDef.severity, created_at=datetime.utcnow(), alarm_def_id=alarmDef.id)
                        alarm.create_in_db(conn.cursor())
                        alarmDefAlarm.update({"alarm": alarm})
                        hadChange = True
                else:
                    if alarm:
                        alarm.status = "RESOLVED"
                        alarm.resolveAlarm(conn.cursor())
                        alarmDefAlarm.update({"alarm": None})
                        hadChange = True
            if hadChange:
                conn.commit()
        
    conn.cursor().execute(
        "UPDATE monitoring_system_var \
        SET \
            value=%s \
        WHERE \
            var=%s \
    ",(last_eleCheck,"last_elecheck"))
    conn.cursor().execute(
        "UPDATE monitoring_system_var \
        SET \
            value=%s \
        WHERE \
            var=%s \
    ",(last_watCheck,"last_watcheck"))
    conn.commit()
        

if __name__ == "__main__":
    PGUSER = os.environ.get("PGUSER")
    PGHOST = os.environ.get("PGHOST")
    PGDATABASE = os.environ.get("PGDATABASE")
    PGPASSWORD = os.environ.get("PGPASSWORD")
    PGPORT = os.environ.get("PGPORT")
    last_eleCheck = datetime.utcnow()
    last_watCheck = datetime.utcnow()
    try:
        conn = psycopg2.connect(
            host=PGHOST,
            database=PGDATABASE,
            user=PGUSER,
            password=PGPASSWORD,
            port=PGPORT
        )
    except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        
    if(conn and createAndInitiateVarTable(conn, last_eleCheck, last_watCheck)):
        try:
            while (True):
                runAlarmCheckAndCreationRoutine(conn)
                time.sleep(10)

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            conn.close()

