import {
  BrowserRouter as Router,
  Routes,
  Route,
} from 'react-router-dom';
import React, { useState } from 'react';

import LoginPage from './components/LoginPage.jsx';
import IndexPage from './components/IndexPage.jsx';
import SignupPage from './components/SignupPage.jsx';
import NotCheckedPage from './components/NotCheckedPage.jsx';
import { AuthContext } from './contexts/index.js';


function AuthProvider({ children }) {
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
}

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="login/" element={<LoginPage />} />
          <Route path="signup/" element={<SignupPage />} />
          <Route path="/" element={(<IndexPage />)} />
          <Route path="/temp" element={(<NotCheckedPage />)} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
