import { Switch, Route, Redirect } from 'react-router-dom';

import Layout from './components/Layout/Layout';
import UserProfile from './components/Profile/UserProfile';
import AuthPage from './pages/AuthPage';
import RegisterGroupPage from './pages/RegisterGroupsPage';
import RegisterListPage from './pages/RegisterListPage';
import MeassureRegisterPage from './pages/MeassureRegisterPage';
import { useContext, useEffect } from 'react';
import AuthContext from './store/auth-context';
import AlarmsPage from './pages/AlarmsPage';
import ReportPage from './pages/ReportPage';

function App() {
  const authCtx = useContext(AuthContext);

  useEffect(() => {
    document.title = 'Monitoramento';
  });

  return (
    <Layout>
      <Switch>
        {authCtx.isLoggedIn && (
          <Route path="/alarms" exact>
            <AlarmsPage />
          </Route>
        )}
        {authCtx.isLoggedIn && (
          <Route path="/registerGroups" exact>
            <RegisterGroupPage />
          </Route>
        )}
        {authCtx.isLoggedIn && (
          <Route path="/registersList" exact>
            <RegisterListPage />
          </Route>
        )}
        {authCtx.isLoggedIn && (
          <Route path="/registersMeassures" exact>
            <MeassureRegisterPage />
          </Route>
        )}
        {!authCtx.isLoggedIn && (
          <Route path="/auth">
            <AuthPage />
          </Route>
        )}
        {authCtx.isLoggedIn && (
          <Route path="/profile">
            <UserProfile />
          </Route>
        )}
        {authCtx.isLoggedIn && (
          <Route path="/report">
            <ReportPage />
          </Route>
        )}
        <Route path="*">
          {authCtx.isLoggedIn ? (
            <Redirect to="/alarms" />
          ) : (
            <Redirect to="/auth" />
          )}
        </Route>
      </Switch>
    </Layout>
  );
}

export default App;
