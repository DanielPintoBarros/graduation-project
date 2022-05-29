import AuthContext from '../store/auth-context';
import { useState, useContext } from 'react';
import { useLocation } from 'react-router-dom';
import classes from './RegisterGroupList.module.css';
import RegistersComponent from '../components/Register/RegistersComponent';
import NewRegisterForm from '../components/Register/NewRegisterForm';

const RegisterListPage = (props) => {
  const authCtx = useContext(AuthContext);
  const [registers, setRegisters] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [openNewRegister, setOpenNewRegister] = useState(false);
  const location = useLocation();

  function fetchRegisters() {
    const regGroupId = location.state.regGroupId;
    fetch(`http://localhost:5000/regGroup/${regGroupId}/registers`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${authCtx.token}`,
      },
    }).then((data) => {
      return data.json().then((regData) => {
        setRegisters(
          regData.registers.map((reg) => {
            return {
              id: reg.id,
              name: reg.name,
              description: reg.description,
              latitude: reg.latitude,
              longitude: reg.longitude,
              register_type: reg.register_type,
              modbus_port: reg.modbus_port,
              register_group_id: reg.register_group_id,
              inDetailPage: false,
            };
          })
        );
        setIsLoading(false);
      });
    });
  }

  if (isLoading) {
    fetchRegisters();
  }

  return (
    <section>
      <div>
        <h1 className={classes.h1}>Medidores do Grupo</h1>
        <button
          className={classes.openModalBtn}
          onClick={() => setOpenNewRegister(true)}
        >
          Add Medidor
        </button>
        {openNewRegister && (
          <NewRegisterForm
            regGroupId={location.state.regGroupId}
            refreshPage={setIsLoading}
            closeModal={setOpenNewRegister}
          />
        )}
      </div>

      {isLoading && <div className={classes.content}>Loading...</div>}
      {!isLoading && registers.length === 0 && (
        <div className={classes.content}>Não foi encontrado nenhum medidor</div>
      )}
      {!isLoading && registers.length > 0 && (
        <ul className={classes.list}>
          <div className={classes.center}>
            {registers.map((register) => {
              return (
                <RegistersComponent
                  key={register.id}
                  register={register}
                  center={false}
                  setIsLoading={setIsLoading}
                />
              );
            })}
          </div>
        </ul>
      )}
    </section>
  );
};

export default RegisterListPage;
