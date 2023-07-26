import React, { useState, useEffect, useCallback } from 'react';

let LOGOUT_TIME;

const AuthContext = React.createContext({
  token: '',
  isLoggedIn: false,

  login: (token) => {},
  logout: () => {},
});

const calculateRemainingTime = (expirationTime) => {
  const currentTime = new Date().getTime();
  return expirationTime - currentTime;
};

const retrieveStoredToken = () => {
  const storedToken = localStorage.getItem('token');
  const storedExpirationDate = localStorage.getItem('expirationTime');

  const remainingTime = calculateRemainingTime(storedExpirationDate);
  if (remainingTime <= 3600) {
    localStorage.removeItem('token');
    localStorage.removeItem('expirationTime');
    return null;
  }
  return { token: storedToken, remainingTime: remainingTime };
};

export const AuthContextProvider = (props) => {
  const tokenData = retrieveStoredToken();
  let initialToken;
  if (tokenData) {
    initialToken = tokenData.token;
  }

  const [token, setToken] = useState(initialToken);
  const userIsLoggedIn = !!token;

  const logoutHandler = useCallback(() => {
    if (token) {
      fetch(`/api/logout`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
      });

      setToken(null);
      localStorage.removeItem('token');
      localStorage.removeItem('expirationTime');

      if (LOGOUT_TIME) {
        clearTimeout(LOGOUT_TIME);
      }
    }
  }, [token]);

  const loginHandler = (token, expirationTime) => {
    setToken(token);
    localStorage.setItem('token', token);
    localStorage.setItem('expirationTime', expirationTime);
    LOGOUT_TIME = setTimeout(
      logoutHandler,
      calculateRemainingTime(expirationTime)
    );
  };

  useEffect(() => {
    if (tokenData) {
      LOGOUT_TIME = setTimeout(logoutHandler, tokenData.remainingTime);
    }
  }, [tokenData, logoutHandler]);

  const contextValue = {
    token: token,
    isLoggedIn: userIsLoggedIn,
    login: loginHandler,
    logout: logoutHandler,
  };

  return (
    <AuthContext.Provider value={contextValue}>
      {props.children}
    </AuthContext.Provider>
  );
};

export default AuthContext;
