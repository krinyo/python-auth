import React, { useContext } from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import Home from './components/Home';
import Login from './components/Login';
import Register from './components/Register';
import Profile from './components/Profile';
import TestResource from './components/TestResource'; // Import new component
import { AuthProvider } from './context/AuthContext';
import AuthContext from './context/AuthContext';
import PrivateRoute from './utils/PrivateRoute';
import './App.css';

// A small helper component for the navbar
const Navbar = () => {
  const { user, logoutUser } = useContext(AuthContext);
  return (
    <nav>
      <ul>
        <li><Link to="/">Home</Link></li>
        {user ? (
          <>
            <li><Link to="/profile">Profile</Link></li>
            <li><Link to="/test-resource">Test Resource</Link></li> {/* Add new link */}
            <li><button onClick={logoutUser}>Logout</button></li>
          </>
        ) : (
          <>
            <li><Link to="/login">Login</Link></li>
            <li><Link to="/register">Register</Link></li>
          </>
        )}
      </ul>
    </nav>
  );
};


function App() {
  return (
    <Router>
      <AuthProvider>
        <div>
          <Navbar />
          <hr />
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route element={<PrivateRoute />}>
              <Route path="/profile" element={<Profile />} />
              <Route path="/test-resource" element={<TestResource />} /> {/* Add new route */}
            </Route>
          </Routes>
        </div>
      </AuthProvider>
    </Router>
  );
}

export default App;
