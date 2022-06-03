import AuthContext from '../store/auth-context';
import { useState, useContext } from 'react';
import { useLocation, Link } from 'react-router-dom';
import classes from './RegisterGroupList.module.css';
import RegistersComponent from '../components/Register/RegistersComponent';
import MeassureItem from '../components/Meassure/MeassureItem';
import AlarmDefinitionItem from '../components/AlarmDefinition/AlarmDefinitionItem';
import NewAlarmDefinitionForm from '../components/AlarmDefinition/NewAlarmDefinitionForm';

const MeassureRegisterPage = () => {
  const location = useLocation();

  const register_id = location.state.register_id;
  const group_id = location.state.group_id;

  const [register, setRegister] = useState({});
  const authCtx = useContext(AuthContext);
  const [alarmDefinitions, setAlarmDefinitions] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isRegisterLoading, setIsRegisterLoading] = useState(true);
  const [openNewAlarmDef, setOpenNewAlarmDef] = useState(false);

  function fetchRegister() {
    fetch(`http://localhost:5000/register/${register_id}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${authCtx.token}`,
      },
    }).then((response) => {
      return response.json().then((data) => {
        setRegister(data.register);
        setIsRegisterLoading(false);
      });
    });
  }
  function fetchAlarmDefinitions() {
    fetch(`http://localhost:5000/register/${register_id}/alarmDefinitions`, {
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

  if (isRegisterLoading) {
    fetchRegister();
  }
  if (isLoading) {
    fetchAlarmDefinitions();
  }

  return (
    <section>
      {isRegisterLoading && <div>Loading...</div>}
      {!isRegisterLoading && (
        <div>
          <header className={classes.headerTopic}>
            <div id="localNavigation">
              <Link
                to={{
                  pathname: '/alarms',
                }}
              >
                Alarms
              </Link>
              {'>'}
              <Link
                to={{
                  pathname: '/registerGroups',
                }}
              >
                Grupos
              </Link>
              {'>'}
              <Link
                to={{
                  pathname: '/registersList',
                  state: { regGroupId: group_id },
                }}
              >
                Medidores
              </Link>
              {'>'}
            </div>
            <h1 className={classes.h1}>Medidor</h1>
          </header>
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
              refresh={!openNewAlarmDef}
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
                register_type={register.register_type}
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
      )}
    </section>
  );
};

export default MeassureRegisterPage;
