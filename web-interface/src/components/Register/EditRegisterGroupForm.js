import { useHistory } from 'react-router-dom';
import AuthContext from '../../store/auth-context';
import { useRef, useContext } from 'react';
import classes from './RegisterGroupItem.module.css';

const EditRegisterGroupForm = (props) => {
  const history = useHistory();

  const authCtx = useContext(AuthContext);

  const nameInputRef = useRef();
  const descriptionInputRef = useRef();

  const submitHandler = (event) => {
    event.preventDefault();

    const enteredName = nameInputRef.current.value;
    const enteredDescription = descriptionInputRef.current.value;

    fetch(`/api/regGroup`, {
      method: 'PUT',
      body: JSON.stringify({
        id: props.id,
        name: enteredName,
        description: enteredDescription,
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
          <h1>Editar Grupo de Medidores</h1>
        </div>
        <div className={classes.body}>
          <form id="editRegGroup" onSubmit={submitHandler}>
            <div className={classes.control}>
              <label htmlFor="name">Name</label>
              <input
                type="text"
                id="name"
                defaultValue={props.name}
                required
                ref={nameInputRef}
              />
            </div>
            <div className={classes.control}>
              <label htmlFor="description">Description</label>
              <input
                type="text"
                id="description"
                required
                defaultValue={props.description}
                ref={descriptionInputRef}
              />
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
          <button type="submit" form="editRegGroup">
            Confirm
          </button>
        </div>
      </div>
    </div>
  );
};

export default EditRegisterGroupForm;
