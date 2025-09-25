import React, { createContext, useState, useEffect } from 'react';
import { jwtDecode } from 'jwt-decode';
import { useNavigate } from 'react-router-dom';
import axiosInstance from '../utils/axiosInstance';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [authTokens, setAuthTokens] = useState(() => localStorage.getItem('authTokens') ? JSON.parse(localStorage.getItem('authTokens')) : null);
  const [user, setUser] = useState(() => localStorage.getItem('authTokens') ? jwtDecode(JSON.parse(localStorage.getItem('authTokens')).access) : null);
  const navigate = useNavigate();

  const loginUser = async (email, password) => {
    const response = await axiosInstance.post('/auth/login/', {
      email,
      password
    });
    if (response.status === 200) {
      setAuthTokens(response.data);
      setUser(jwtDecode(response.data.access));
      localStorage.setItem('authTokens', JSON.stringify(response.data));
      navigate('/profile');
    }
    return response;
  };

  const logoutUser = () => {
    setAuthTokens(null);
    setUser(null);
    localStorage.removeItem('authTokens');
    navigate('/login');
  };

  const contextData = {
    user,
    authTokens,
    loginUser,
    logoutUser,
  };

  // Add a check for token expiration on load
  useEffect(() => {
    if (authTokens) {
        const decoded = jwtDecode(authTokens.access);
        // Simple check if token is expired
        if (decoded.exp * 1000 < Date.now()) {
            logoutUser();
        } else {
            setUser(decoded);
        }
    }
  }, [authTokens]);


  return (
    <AuthContext.Provider value={contextData}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;
