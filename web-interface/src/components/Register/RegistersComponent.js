import { Link } from 'react-router-dom';
import { useState } from 'react';
import classes from './RegisterGroupItem.module.css';
import DeleteRegisterForm from './DeleteRegisterForm';

const RegisterComponent = (props) => {
  const [openDeleteRegister, setOpenDeleteRegister] = useState(false);

  return (
    <li className={props.center ? classes.unique : classes.item}>
      <header className={classes.buttonCardHeader}>
        <button
          className={classes.openModalBtn}
          onClick={() => setOpenDeleteRegister(true)}
        >
          Excluir
        </button>
        {openDeleteRegister && (
          <DeleteRegisterForm
            regGroupId={props.register.register_group_id}
            regId={props.register.id}
            refreshPage={props.setIsLoading}
            closeModal={setOpenDeleteRegister}
          />
        )}
      </header>
      <div className={classes.content}>
        <h3>{props.register.name}</h3>
        <p>{props.register.description}</p>
        <p>Latitude: {props.register.latitude}</p>
        <p>Longitude: {props.register.longitude}</p>
        <p>Tipo do medidor: {props.register.register_type}</p>
        {props.register.modbus_port && (
          <p>Modbus Port {props.register.modbus_port}</p>
        )}
      </div>
      {!props.center && (
        <div className={classes.actions}>
          <Link
            to={{
              pathname: '/registersMeassures',
              state: {
                register_id: props.register.id,
                group_id: props.register.register_group_id,
              },
            }}
          >
            <button>Ver detalhes</button>
          </Link>
        </div>
      )}
    </li>
  );
};

export default RegisterComponent;
