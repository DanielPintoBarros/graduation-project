import AuthContext from '../store/auth-context';
import { useState, useContext } from 'react';
import classes from './RegisterGroupList.module.css';
import RegisterGroupItem from '../components/Register/RegisterGroupItem';
import NewRegisterGroupForm from '../components/Register/NewRegisterGroupForm';
import { Link } from 'react-router-dom';

const RegisterGroupPage = () => {
  const [openNewRegGroup, setOpenNewRegGroup] = useState(false);

  const authCtx = useContext(AuthContext);
  const [groups, setGroups] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  function fetchRegisterGroups() {
    fetch(`/api/regGroup`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${authCtx.token}`,
      },
    }).then((data) => {
      return data.json().then((groupsData) => {
        setGroups(
          groupsData.groups.map((group) => {
            return {
              id: group.id,
              name: group.name,
              description: group.description,
            };
          })
        );
        setIsLoading(false);
      });
    });
  }

  if (isLoading) {
    fetchRegisterGroups();
  }

  return (
    <section>
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
        </div>
        <h1 className={classes.h1}>Grupos de Medidores</h1>
        <button
          className={classes.openModalBtn}
          onClick={() => setOpenNewRegGroup(true)}
        >
          Create Group
        </button>
        {openNewRegGroup && (
          <NewRegisterGroupForm
            refreshPage={setIsLoading}
            closeModal={setOpenNewRegGroup}
          />
        )}
      </header>
      {isLoading && <div className={classes.content}>Loading...</div>}
      {!isLoading && groups.length === 0 && (
        <div className={classes.content}>Não foi encontrado nenhum grupo</div>
      )}
      {!isLoading && groups.length > 0 && (
        <ul className={classes.list}>
          <div className={classes.center}>
            {groups.map((group) => {
              return (
                <RegisterGroupItem
                  key={group.id}
                  group={group}
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

export default RegisterGroupPage;
