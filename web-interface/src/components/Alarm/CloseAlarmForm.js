import AuthContext from '../../store/auth-context';
import { useContext } from 'react';
import classes from './AlarmCloseForm.module.css';

const CloseAlarmForm = (props) => {
  const authCtx = useContext(AuthContext);

  const submitHandler = (event) => {
    event.preventDefault();

    fetch(`/api/closeAlarm/${props.id}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${authCtx.token}`,
      },
    }).then((res) => {
      props.closeModal(false);
      props.refreshPage(true);
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
          <h1>Desativar Alarme</h1>
        </div>
        <div className={classes.body}>
          <form id="closeAlarm" onSubmit={submitHandler}>
            <div className={classes.control}>
              <p>Tem certeza que deseja desativar o alarme?</p>
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
          <button type="submit" form="closeAlarm">
            Confirm
          </button>
        </div>
      </div>
    </div>
  );
};

export default CloseAlarmForm;
