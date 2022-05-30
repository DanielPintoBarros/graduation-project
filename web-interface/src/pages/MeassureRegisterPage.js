import AuthContext from '../store/auth-context';
import { useState, useContext } from 'react';
import { useLocation } from 'react-router-dom';
import classes from './RegisterGroupList.module.css';
import RegistersComponent from '../components/Register/RegistersComponent';
import MeassureItem from '../components/Meassure/MeassureItem';
import AlarmDefinitionItem from '../components/AlarmDefinition/AlarmDefinitionItem';
import NewAlarmDefinitionForm from '../components/AlarmDefinition/NewAlarmDefinitionForm';

const MeassureRegisterPage = () => {
  const location = useLocation();

  const register = location.state.register;

  const authCtx = useContext(AuthContext);
  const [alarmDefinitions, setAlarmDefinitions] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [openNewAlarmDef, setOpenNewAlarmDef] = useState(false);

  function fetchAlarmDefinitions() {
    fetch(`http://localhost:5000/register/${register.id}/alarmDefinitions`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${authCtx.token}`,
      },
    }).then((response) => {
      return response.json().then((data) => {
        setAlarmDefinitions(data.alarmDef);
        setIsLoading(false);
      });
    });
  }

  if (isLoading) {
    fetchAlarmDefinitions();
  }

  return (
    <section>
      <div>
        <h1 className={classes.h1}>Medidor</h1>
        <ul className={classes.list}>
          <RegistersComponent
            key={register.id}
            register={register}
            center={true}
          />
        </ul>
        <h1 className={classes.h1}>Última medida</h1>
        <ul className={classes.list}>
          <MeassureItem
            key={register.id}
            register_id={register.id}
            register_type={register.register_type}
          />
        </ul>
        <header className={classes.headerTopic}>
          <h1 className={classes.h1}>Definição de alarmes</h1>
          <button
            className={classes.openModalBtn}
            onClick={() => setOpenNewAlarmDef(true)}
          >
            Criar AlarmDef
          </button>
          {openNewAlarmDef && (
            <NewAlarmDefinitionForm
              register_id={register.id}
              refreshPage={setIsLoading}
              closeModal={setOpenNewAlarmDef}
            />
          )}
        </header>
        {isLoading && <div className={classes.content}>Loading...</div>}
        {!isLoading && alarmDefinitions.length === 0 && (
          <div className={classes.content}>
            Nenhuma definição de alarme foi encontrada
          </div>
        )}
        {!isLoading && alarmDefinitions.length > 0 && (
          <ul className={classes.list}>
            <div className={classes.center}>
              {alarmDefinitions.map((alarmDef) => {
                return (
                  <AlarmDefinitionItem
                    key={alarmDef.id}
                    alarmDef={alarmDef}
                    setIsLoading={setIsLoading}
                  />
                );
              })}
            </div>
          </ul>
        )}
      </div>
    </section>
  );
};

export default MeassureRegisterPage;
