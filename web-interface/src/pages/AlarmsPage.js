import classes from './RegisterGroupList.module.css';

import AuthContext from '../store/auth-context';
import { useState, useContext, useEffect } from 'react';

import AlarmRow from '../components/Alarm/AlarmRow';

const AlarmsPage = () => {
  const authCtx = useContext(AuthContext);
  const [alarms, setAlarms] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isAlarmsLoading, setIsAlarmsLoading] = useState(true);

  useEffect(() => {
    if (!isAlarmsLoading) {
      setTimeout(() => {
        setIsAlarmsLoading(true);
      }, 10000);
    }
  });
  function fetchAlarms() {
    fetch('http://localhost:5000/openAlarms', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${authCtx.token}`,
      },
    }).then((response) => {
      response.json().then((data) => {
        setAlarms(
          data.alarms.map((alarm) => {
            return {
              id: alarm.id,
              description: alarm.description,
              status: alarm.status,
              severity: alarm.severity,
              created_at: alarm.created_at,
              register_name: alarm.register_name,
              register_id: alarm.register_id,
            };
          })
        );
        setIsLoading(false);
        setIsAlarmsLoading(false);
      });
    });
  }
  if (isLoading || isAlarmsLoading) {
    fetchAlarms();
  }

  return (
    <section>
      <header className={classes.headerTopic}>
        <h1 className={classes.h1}>Alarmes</h1>
      </header>
      {isLoading && <div>Loading</div>}
      {!isLoading && (
        <table className={classes.alarms}>
          <thead>
            <tr>
              <th>Descrição</th>
              <th className={classes.alarmsSeverity}>Severidade</th>
              <th className={classes.alarmsState}>Estado</th>
              <th className={classes.alarmsCreatedAt}>Criado em</th>
              <th className={classes.alarmsRegister}>Medidor</th>
              <th className={classes.alarmsAction}>Ações</th>
            </tr>
          </thead>
          <tbody>
            {alarms.map((alarm) => {
              return (
                <AlarmRow
                  key={alarm.id}
                  alarm={alarm}
                  setIsLoading={setIsLoading}
                />
              );
            })}
          </tbody>
        </table>
      )}
    </section>
  );
};

export default AlarmsPage;
