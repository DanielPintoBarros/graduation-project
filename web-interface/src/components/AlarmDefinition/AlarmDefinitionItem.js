import classes from './AlarmDefinitionItem.module.css';
import DeleteAlarmDefinitionForm from './DeleteAlarmDefinitionForm';
import { useState } from 'react';

const translateSeverity = (severity) => {
  if (severity === 'CRITICAL') {
    return 'Crítico';
  } else if (severity === 'WARNING') {
    return 'Aviso';
  } else {
    return severity;
  }
};

const serializeAttributes = (alarmDef) => {
  const translateKey = (key) => {
    switch (key) {
      case 'w_thr':
        return 'Limite Potência Ativa';
      case 'va_thr':
        return 'Limite Potência Aparente';
      case 'irms_thr':
        return 'Limite Corrente rms';
      case 'vrms_thr':
        return 'Limite Tensão rms';
      case 'fp_thr':
        return 'Limite Fator de Potência';
      case 'E_thr':
        return 'Limite Energia Consumida';
      case 'energyInterval':
        return 'Intervalo de Consumo de Energia';
      case 'value_thr':
        return 'Limite Consumo de Água';
      case 'waterInterval':
        return 'Intervalo de Consumo de Água';
      default:
        return null;
    }
  };

  const paramArray = [];
  Object.keys(alarmDef).forEach((param) => {
    const translatedKey = translateKey(param);
    if (translatedKey) {
      paramArray.push({
        key: translatedKey,
        value: alarmDef[param],
        originalKey: param,
      });
    }
  });

  return paramArray;
};

const AlarmDefinitionItem = (props) => {
  const [openDeleteAlarmDef, setOpenDeleteAlarmDef] = useState(false);

  return (
    <li className={classes.item}>
      <header className={classes.buttonCardHeader}>
        <button
          className={classes.openModalBtn}
          onClick={() => setOpenDeleteAlarmDef(true)}
        >
          Excluir
        </button>
        {openDeleteAlarmDef && (
          <DeleteAlarmDefinitionForm
            id={props.alarmDef.id}
            refreshPage={props.setIsLoading}
            closeModal={setOpenDeleteAlarmDef}
          />
        )}
      </header>
      <div className={classes.content}>
        <p key="description">
          <b>Descrição: </b>
          {props.alarmDef.description}
        </p>
        <p key="severity">
          <b>Severidade: </b> {translateSeverity(props.alarmDef.severity)}
        </p>
        {serializeAttributes(props.alarmDef).map((item) => {
          return (
            <p key={item.originalKey}>
              <b>{item.key}:</b> {item.value}
            </p>
          );
        })}
      </div>
    </li>
  );
};

export default AlarmDefinitionItem;
