import AuthContext from '../../store/auth-context';
import { useRef, useContext } from 'react';
import classes from './AlarmDefinitionItem.module.css';

const NewAlarmDefinitionForm = (props) => {
  const authCtx = useContext(AuthContext);

  const descriptionInputRef = useRef();
  const severityInputRef = useRef();
  const wthrInputRef = useRef();
  const vathrInputRef = useRef();
  const vrmsthrInputRef = useRef();
  const irmsthrInputRef = useRef();
  const fpthrInputRef = useRef();
  const ethrInputRef = useRef();
  const waterConsumeInputRef = useRef();
  const waterIntervalInputRef = useRef();

  const submitHandler = (event) => {
    event.preventDefault();

    const enteredDescription = descriptionInputRef.current.value;
    const enteredSeverity = severityInputRef.current.value;

    const body = {
      description: enteredDescription,
      register_id: props.register_id,
      severity: enteredSeverity,
    };
    if (wthrInputRef.current) {
      body.w_thr = parseInt(wthrInputRef.current.value);
    }
    if (vathrInputRef.current) {
      body.va_thr = parseInt(vathrInputRef.current.value);
    }
    if (vrmsthrInputRef.current) {
      body.vrms_thr = parseInt(vrmsthrInputRef.current.value);
    }
    if (irmsthrInputRef.current) {
      body.irms_thr = parseInt(irmsthrInputRef.current.value);
    }
    if (fpthrInputRef.current) {
      body.fp_thr = parseInt(fpthrInputRef.current.value);
    }
    if (ethrInputRef.current) {
      body.e_thr = parseInt(ethrInputRef.current.value);
    }
    if (waterConsumeInputRef.current) {
      body.water_consume = parseInt(waterConsumeInputRef.current.value);
    }
    if (waterIntervalInputRef.current) {
      body.water_interval = parseInt(waterIntervalInputRef.current.value);
    }

    fetch(`http://localhost:5000/alarmDefinitions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${authCtx.token}`,
      },
      body: JSON.stringify(body),
    }).then((res) => {
      if (res.ok) {
        props.closeModal(false);
        props.refreshPage(true);
      }
    });
  };

  return (
    <div className={classes.modalBackground}>
      <div className={classes.modalContainer}>
        <div className={classes.titleCloseBtn}>
          <button
            className={classes.button}
            onClick={() => props.closeModal(false)}
          >
            X
          </button>
        </div>
        <div className={classes.title}>
          <h1>Criar Definição de Alarme</h1>
        </div>
        <div className={classes.body}>
          <form id="createAlarmDef" onSubmit={submitHandler}>
            <div className={classes.control}>
              <label htmlFor="description">Descrição</label>
              <input
                type="text"
                id="description"
                required
                ref={descriptionInputRef}
              />
            </div>
            <div className={classes.control}>
              <label htmlFor="severity">Severidade</label>
              <select
                name="severity"
                id="severity"
                required
                ref={severityInputRef}
              >
                <option value="CRITICAL">Crítico</option>
                <option value="WARNING">Aviso</option>
              </select>
            </div>
            {props.register_type.includes('ENERGY') && (
              <div>
                <div className={classes.control}>
                  <label htmlFor="w_thr">Limite potencia ativa - W</label>
                  <input type="text" id="w_thr" ref={wthrInputRef} />
                </div>
                <div className={classes.control}>
                  <label htmlFor="va_thr">Limite potencia aparente - VA</label>
                  <input type="text" id="va_thr" ref={vathrInputRef} />
                </div>
                <div className={classes.control}>
                  <label htmlFor="vrms_thr">Limite Tensão rms - Vrms</label>
                  <input type="text" id="vrms_thr" ref={vrmsthrInputRef} />
                </div>
                <div className={classes.control}>
                  <label htmlFor="irms_thr">Limite Corrente rms - Irms</label>
                  <input type="text" id="irms_thr" ref={irmsthrInputRef} />
                </div>
                <div className={classes.control}>
                  <label htmlFor="fp_thr">
                    Limite do Fator de Potência - fp
                  </label>
                  <input type="text" id="fp_thr" ref={fpthrInputRef} />
                </div>
                <div className={classes.control}>
                  <label htmlFor="e_thr">
                    Limite do energia consumida - kwh
                  </label>
                  <input type="text" id="e_thr" ref={ethrInputRef} />
                </div>
              </div>
            )}
            {props.register_type.includes('WATER') && (
              <div>
                <div className={classes.control}>
                  <label htmlFor="water_consume">
                    Limite Consumo de agua entre intervalos - L
                  </label>
                  <input
                    type="text"
                    id="water_consume"
                    ref={waterConsumeInputRef}
                  />
                </div>
                <div className={classes.control}>
                  <label htmlFor="water_interval">
                    Intervalo de consumo de agua em horas - dT
                  </label>
                  <input
                    type="text"
                    id="water_interval"
                    ref={waterIntervalInputRef}
                  />
                </div>
              </div>
            )}
          </form>
        </div>
        <div className={classes.footer}>
          <button
            className={classes.button}
            onClick={() => props.closeModal(false)}
          >
            Cancel
          </button>
          <button type="submit" form="createAlarmDef">
            Confirm
          </button>
        </div>
      </div>
    </div>
  );
};

export default NewAlarmDefinitionForm;
