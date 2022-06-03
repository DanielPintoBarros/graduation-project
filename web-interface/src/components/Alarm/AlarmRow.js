import classes from './AlarmRowItem.module.css';
import { useState } from 'react';
import { Link } from 'react-router-dom';
import CloseAlarmForm from './CloseAlarmForm';

const translateSeverity = (severity) => {
  if (severity === 'CRITICAL') {
    return 'Crítico';
  } else if (severity === 'WARNING') {
    return 'Aviso';
  } else {
    return severity;
  }
};

const translateStatus = (status) => {
  if (status === 'RESOLVED') {
    return 'Desativado';
  } else if (status === 'ACTIVE') {
    return 'Ativado';
  } else {
    return status;
  }
};

const AlarmRow = (props) => {
  const [openCloseAlarm, setOpenCloseAlarm] = useState(false);

  return (
    <tr key={props.alarm.id}>
      <td>{props.alarm.description}</td>
      <td className={classes.center}>
        {translateSeverity(props.alarm.severity)}
      </td>
      <td className={classes.center}>{translateStatus(props.alarm.status)}</td>
      <td className={classes.center}>{props.alarm.created_at}</td>
      <td className={classes.center}>
        <Link
          to={{
            pathname: '/registersMeassures',
            state: { register_id: props.alarm.register_id },
          }}
        >
          {props.alarm.register_name}
        </Link>
      </td>
      <td>
        <button
          className={classes.openModalBtn}
          onClick={() => setOpenCloseAlarm(true)}
        >
          Fechar Alarme
        </button>
        {openCloseAlarm && (
          <CloseAlarmForm
            id={props.alarm.id}
            refreshPage={props.setIsLoading}
            closeModal={setOpenCloseAlarm}
          />
        )}
      </td>
    </tr>
  );
};

export default AlarmRow;
