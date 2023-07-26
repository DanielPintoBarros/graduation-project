import { useHistory } from 'react-router-dom';
import AuthContext from '../../store/auth-context';
import { useRef, useContext } from 'react';
import classes from './ReportConfigButtonForm.module.css';

const ReportConfigButtonForm = (props) => {
  const history = useHistory();

  const authCtx = useContext(AuthContext);

  const dayInputRef = useRef();

  const submitHandler = (event) => {
    event.preventDefault();

    fetch(`/api/reportMeassures/${props.regId}`, {
      method: 'POST',
      body: JSON.stringify({
        day: dayInputRef.current.value,
      }),
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${authCtx.token}`,
      },
    }).then((res) => {
      if (res.ok) {
        res.json().then((data) => {
          props.closeModal(false);
          if (history.location.pathname === '/report') {
            props.setMeassures(data.meassures);
          } else {
            history.replace('/report', {
              meassures: data.meassures,
              register: data.register,
            });
          }
        });
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
          <h1>Gerar Gráficos</h1>
        </div>
        <div className={classes.body}>
          <form id="createRegGroup" onSubmit={submitHandler}>
            <div className={classes.control}>
              <label htmlFor="day">Data</label>
              <input type="date" id="day" required ref={dayInputRef} />
            </div>
          </form>
        </div>
        <div className={classes.footer}>
          <button
            className={classes.button}
            onClick={() => props.closeModal(false)}
          >
            Cancel
          </button>
          <button type="submit" form="createRegGroup">
            Confirm
          </button>
        </div>
      </div>
    </div>
  );
};

export default ReportConfigButtonForm;
