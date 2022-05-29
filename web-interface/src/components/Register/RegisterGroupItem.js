import { Link } from 'react-router-dom';
import { useState } from 'react';
import classes from './RegisterGroupItem.module.css';
import EditRegisterGroupForm from './EditRegisterGroupForm';
import DeleteRegisterGroupForm from './DeleteRegisterGroupForm';

const RegisterGroupItem = (props) => {
  const [openEditRegGroup, setOpenEditRegGroup] = useState(false);
  const [openDeleteRegGroup, setOpenDeleteRegGroup] = useState(false);

  return (
    <li className={classes.item}>
      <div>
        <button
          className={classes.openModalBtn}
          onClick={() => setOpenEditRegGroup(true)}
        >
          Edit
        </button>
        {openEditRegGroup && (
          <EditRegisterGroupForm
            id={props.group.id}
            name={props.group.name}
            description={props.group.description}
            refreshPage={props.setIsLoading}
            closeModal={setOpenEditRegGroup}
          />
        )}
        <button
          className={classes.openModalBtn}
          onClick={() => setOpenDeleteRegGroup(true)}
        >
          Excluir
        </button>
        {openDeleteRegGroup && (
          <DeleteRegisterGroupForm
            id={props.group.id}
            refreshPage={props.setIsLoading}
            closeModal={setOpenDeleteRegGroup}
          />
        )}
      </div>
      <div className={classes.content}>
        <h3>{props.group.name}</h3>
        <p>{props.group.description}</p>
      </div>
      <div className={classes.actions}>
        <Link
          to={{
            pathname: '/registersList',
            state: { regGroupId: props.group.id },
          }}
        >
          <button>Ver grupo</button>
        </Link>
      </div>
    </li>
  );
};

export default RegisterGroupItem;
