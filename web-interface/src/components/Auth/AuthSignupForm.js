import classes from './AuthForm.module.css';
import { useState, useRef } from 'react';
import { useHistory } from 'react-router-dom';

const AuthSignupForm = () => {
  const history = useHistory();
  const emailInputRef = useRef();
  const passwordInputRef = useRef();
  const confirmPasswordInputRef = useRef();
  const firstNameInputRef = useRef();
  const lastNameInputRef = useRef();

  const [isLoading, setIsLoading] = useState(false);

  const submitHandler = (event) => {
    event.preventDefault();

    const enteredEmail = emailInputRef.current.value;
    const enteredPassword = passwordInputRef.current.value;
    const enteredConfirmPassword = confirmPasswordInputRef.current.value;
    const enteredFirstName = firstNameInputRef.current.value;
    const enteredLastName = lastNameInputRef.current.value;

    if (enteredPassword !== enteredConfirmPassword) {
      alert('The passwords are not matching!');
    } else {
      setIsLoading(true);
      fetch(`/api/signup`, {
        method: 'POST',
        body: JSON.stringify({
          email: enteredEmail,
          password: enteredPassword,
          first_name: enteredFirstName,
          last_name: enteredLastName,
        }),
        headers: {
          'Content-Type': 'application/json',
        },
      }).then((res) => {
        setIsLoading(false);
        res.json().then((data) => {
          alert(data.message);
        });
        if (res.ok) {
          history.replace('/auth');
        }
      });
    }
  };

  return (
    <div>
      <h1>Sign Up</h1>
      <form onSubmit={submitHandler}>
        <div className={classes.control}>
          <label htmlFor="email">Email</label>
          <input type="email" id="email" required ref={emailInputRef} />
        </div>
        <div className={classes.control}>
          <label htmlFor="password">Senha</label>
          <input
            type="password"
            id="password"
            required
            ref={passwordInputRef}
          />
        </div>
        <div className={classes.control}>
          <label htmlFor="password_confirm">Confirme sua senha</label>
          <input
            type="password"
            id="password_confirm"
            required
            ref={confirmPasswordInputRef}
          />
        </div>
        <div className={classes.control}>
          <label htmlFor="first_name">Nome</label>
          <input type="text" id="first_name" required ref={firstNameInputRef} />
        </div>
        <div className={classes.control}>
          <label htmlFor="last_name">Sobrenome</label>
          <input type="text" id="last_name" required ref={lastNameInputRef} />
        </div>
        <div className={classes.actions}>
          {!isLoading && <button>Criar Conta</button>}
          {isLoading && <p>Enviando requisição...</p>}
        </div>
      </form>
    </div>
  );
};

export default AuthSignupForm;
