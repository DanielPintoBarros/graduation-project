import AuthContext from '../../store/auth-context';
import { useContext } from 'react';
import classes from './AlarmDefinitionItem.module.css';

const DeleteAlarmDefinitionForm = (props) => {
  const authCtx = useContext(AuthContext);

  const submitHandler = (event) => {
    event.preventDefault();

    fetch(`http://localhost:5000/alarmDefinitions/${props.id}`, {
      method: 'DELETE',
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
          <h1>Excluir Definição de Alarme</h1>
        </div>
        <div className={classes.body}>
          <form id="deleteAlarmDef" onSubmit={submitHandler}>
            <div className={classes.control}>
              <p>Tem certeza que deseja deletar essa definição?</p>
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
          <button type="submit" form="deleteAlarmDef">
            Confirm
          </button>
        </div>
      </div>
    </div>
  );
};

export default DeleteAlarmDefinitionForm;
