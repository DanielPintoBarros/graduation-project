import { useHistory } from 'react-router-dom';
import AuthContext from '../../store/auth-context';
import { useRef, useContext } from 'react';
import classes from './RegisterGroupItem.module.css';

const NewRegisterGroupForm = (props) => {
  const history = useHistory();

  const authCtx = useContext(AuthContext);

  const nameInputRef = useRef();
  const descriptionInputRef = useRef();
  const latitudeInputRef = useRef();
  const longitudeInputRef = useRef();
  const registerTypeInputRef = useRef();
  const modbusPortInputRef = useRef();

  const submitHandler = (event) => {
    event.preventDefault();

    const enteredName = nameInputRef.current.value;
    const enteredDescription = descriptionInputRef.current.value;
    const enteredLatitude = latitudeInputRef.current.value;
    const enteredLongitude = longitudeInputRef.current.value;
    const enteredRegisterType = registerTypeInputRef.current.value;
    const enteredModbusPort = modbusPortInputRef.current.value;

    const body = {
      name: enteredName,
      description: enteredDescription,
      latitude: enteredLatitude,
      longitude: enteredLongitude,
      register_type: enteredRegisterType,
      register_group_id: props.regGroupId,
    };

    if (enteredModbusPort) {
      body.modbus_port = enteredModbusPort;
    }
    fetch('http://localhost:5000/register', {
      method: 'POST',
      body: JSON.stringify(body),
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${authCtx.token}`,
      },
    }).then((res) => {
      res.json().then((data) => {
        alert(
          `Atenção! Salve essas credenciais para conectar o medidor na rede\n
          Email: ${data['credentials-access'].email}\n
          Senha: ${data['credentials-access'].password}`
        );
        props.closeModal(false);
        props.refreshPage(true);
        if (res.ok) {
          history.replace('/registersList', { regGroupId: props.regGroupId });
        }
      });
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
          <h1>Criar Medidor</h1>
        </div>
        <div className={classes.body}>
          <form id="createRegister" onSubmit={submitHandler}>
            <div className={classes.control}>
              <label htmlFor="name">Nome</label>
              <input type="text" id="name" required ref={nameInputRef} />
            </div>
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
              <label htmlFor="latitude">Latitude</label>
              <input
                type="text"
                id="latitude"
                required
                ref={latitudeInputRef}
              />
            </div>
            <div className={classes.control}>
              <label htmlFor="longitude">Longitude</label>
              <input
                type="text"
                id="longitude"
                required
                ref={longitudeInputRef}
              />
            </div>
            <div className={classes.control}>
              <label htmlFor="registerType">Tipo do medidor</label>
              <div className={classes.customSelect}>
                <select
                  name="registerType"
                  id="registerType"
                  required
                  ref={registerTypeInputRef}
                >
                  <option value="ENERGY1">Elétrico monofásico</option>
                  <option value="ENERGY2">Elétrico bifásico</option>
                  <option value="ENERGY3">Elétrico trifásico</option>
                  <option value="WATER">Consumo de água</option>
                </select>
              </div>
            </div>
            <div className={classes.control}>
              <label htmlFor="modbusPort">Porta do Modbus (opcional)</label>
              <input type="text" id="modbusPort" ref={modbusPortInputRef} />
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
          <button type="submit" form="createRegister">
            Confirm
          </button>
        </div>
      </div>
    </div>
  );
};

export default NewRegisterGroupForm;
