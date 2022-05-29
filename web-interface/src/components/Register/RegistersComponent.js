import { Link } from 'react-router-dom';
import { useState } from 'react';
import classes from './RegisterGroupItem.module.css';
import DeleteRegisterForm from './DeleteRegisterForm';

const RegisterComponent = (props) => {
  const [openDeleteRegister, setOpenDeleteRegister] = useState(false);

  return (
    <li className={props.center ? classes.unique : classes.item}>
      <div>
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
      </div>
      <div className={classes.content}>
        <h3>{props.register.description}</h3>
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
              state: { register: props.register },
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
