import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
  useLocation,
} from 'react-router-dom';
import React, { useState, useEffect } from "react";

import LoginPage from './components/LoginPage.jsx';
import IndexPage from './components/IndexPage.jsx';
import SignupPage from './components/SignupPage.jsx';

import useAuth from './hooks/index.js';
import { AuthContext } from './contexts/index.js';
import { validateToken } from './utils/requests.js';
import SpinnerEl from './components/Spinner.jsx';


const AuthProvider = ({ children }) => {
  const [loggedIn, setLoggedIn] = useState(false);
  const logIn = () => setLoggedIn(true);
  const logOut = () => {
    localStorage.removeItem('user');
    setLoggedIn(false);
  };
  return (
    <AuthContext.Provider value={{ loggedIn, logIn, logOut }}>
      {children}
    </AuthContext.Provider>
  );
};

const PrivateRoute = ({ children }) => {
  const auth = useAuth();
  const location = useLocation();
  const [loading, setLoading] = useState(true);

  const access_token = localStorage.getItem('user')

  useEffect(() => {
    const inner = async () => {
      auth.loggedIn = await validateToken(access_token)
      setLoading(false);
    }
    inner();
  }, []);

  if (!access_token) {
    return <Navigate to="/login" state={{ from: location }} />
  }

  const content = auth.loggedIn ? children : <Navigate to="/login" state={{ from: location }} />
  return loading ? <SpinnerEl/> : content;
};

function App() {
  return (
        <AuthProvider>
            <Router>
              <Routes>
                <Route path="login/" element={<LoginPage />} />
                <Route path="signup/" element={<SignupPage />} />
                <Route
                  path="/"
                  element={(
                  <PrivateRoute>
                    <IndexPage />
                  </PrivateRoute>
                  )}
                />  
              </Routes>
            </Router>
        </AuthProvider>
  );
}

export default App;
