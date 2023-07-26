import { useHistory } from 'react-router-dom';
import AuthContext from '../../store/auth-context';
import { useContext } from 'react';
import classes from './RegisterGroupItem.module.css';

const DeleteRegisterForm = (props) => {
  const history = useHistory();

  const authCtx = useContext(AuthContext);

  const submitHandler = (event) => {
    event.preventDefault();

    fetch(`/api/register/${props.regId}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${authCtx.token}`,
      },
    }).then((res) => {
      props.closeModal(false);
      props.refreshPage(true);
      if (res.ok) {
        history.replace('/registersList', { regGroupId: props.regGroupId });
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
          <h1>Excluir Medidor</h1>
        </div>
        <div className={classes.body}>
          <form id="deleteRegister" onSubmit={submitHandler}>
            <div className={classes.control}>
              <p>Tem certeza que deseja deletar esse medidor?</p>
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
          <button type="submit" form="deleteRegister">
            Confirm
          </button>
        </div>
      </div>
    </div>
  );
};

export default DeleteRegisterForm;
