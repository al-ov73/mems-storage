import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
  useLocation,
} from 'react-router-dom';
import React, { useState } from 'react';

import LoginPage from './components/LoginPage.jsx';
import IndexPage from './components/IndexPage.jsx';
import SignupPage from './components/SignupPage.jsx';

import useAuth from './hooks/index.js';
import { AuthContext } from './contexts/index.js';


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
  if (localStorage.getItem('user')) {
    auth.loggedIn = true;
  }
  return (
    auth.loggedIn ? children : <Navigate to="/login" state={{ from: location }} />
  );
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
