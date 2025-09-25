import React, { useContext } from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import AuthContext from '../context/AuthContext';

const PrivateRoute = () => {
  const { user } = useContext(AuthContext);
  
  // If the user is authenticated, render the child routes.
  // Otherwise, redirect to the login page.
  return user ? <Outlet /> : <Navigate to="/login" />;
};

export default PrivateRoute;
