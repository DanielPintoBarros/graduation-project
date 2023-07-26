import { useState } from 'react';

import classes from './AuthForm.module.css';
import AuthLoginForm from './AuthLoginForm';
import AuthSignupForm from './AuthSignupForm';

const AuthForm = () => {
  const [isLogin, setIsLogin] = useState(true);

  const switchAuthModeHandler = () => {
    setIsLogin((prevState) => !prevState);
  };

  return (
    <section className={classes.auth}>
      {isLogin ? <AuthLoginForm /> : <AuthSignupForm />}
      <div className={classes.actions}>
        <button
          type="button"
          className={classes.toggle}
          onClick={switchAuthModeHandler}
        >
          {isLogin ? 'Criar nova conta' : 'Entrar com contra já criada'}
        </button>
      </div>
    </section>
  );
};

export default AuthForm;
