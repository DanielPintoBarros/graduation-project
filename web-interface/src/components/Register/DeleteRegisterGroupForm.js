import { useHistory } from 'react-router-dom';
import AuthContext from '../../store/auth-context';
import { useContext } from 'react';
import classes from './RegisterGroupItem.module.css';

const DeleteRegisterGroupForm = (props) => {
  const history = useHistory();

  const authCtx = useContext(AuthContext);

  const submitHandler = (event) => {
    event.preventDefault();

    fetch(`http://localhost:5000/regGroup`, {
      method: 'DELETE',
      body: JSON.stringify({
        id: props.id,
      }),
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${authCtx.token}`,
      },
    }).then((res) => {
      props.closeModal(false);
      props.refreshPage(true);
      if (res.ok) {
        history.replace('/registerGroups');
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
          <h1>Excluir Grupo</h1>
        </div>
        <div className={classes.body}>
          <form id="deleteRegGroup" onSubmit={submitHandler}>
            <div className={classes.control}>
              <p>Tem certeza que deseja deletar o grupo?</p>
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
          <button type="submit" form="deleteRegGroup">
            Confirm
          </button>
        </div>
      </div>
    </div>
  );
};

export default DeleteRegisterGroupForm;
