import React, { useState } from 'react';
import axiosInstance from '../utils/axiosInstance';

function Register() {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    password2: ''
  });
  const [message, setMessage] = useState('');

  const { username, email, password, password2 } = formData;

  const onChange = e => setFormData({ ...formData, [e.target.name]: e.target.value });

  const onSubmit = async e => {
    e.preventDefault();
    if (password !== password2) {
      setMessage('Passwords do not match');
      return;
    }
    try {
      const res = await axiosInstance.post('/auth/register/', {
        username,
        email,
        password,
        password2
      });
      setMessage('User registered successfully! Please log in.');
      console.log(res.data);
    } catch (err) {
      // Extract and display backend errors
      const errors = err.response.data;
      let errorMsg = 'Error registering user. ';
      if (errors) {
        // Flatten all error messages into a single string
        errorMsg += Object.values(errors).flat().join(' ');
      }
      setMessage(errorMsg);
      console.error(err.response.data);
    }
  };

  return (
    <div>
      <h2>Register</h2>
      <form onSubmit={onSubmit}>
        <div>
          <input
            type="text"
            placeholder="Username"
            name="username"
            value={username}
            onChange={onChange}
            required
          />
        </div>
        <div>
          <input
            type="email"
            placeholder="Email Address"
            name="email"
            value={email}
            onChange={onChange}
            required
          />
        </div>
        <div>
          <input
            type="password"
            placeholder="Password"
            name="password"
            value={password}
            onChange={onChange}
            minLength="8"
            required
          />
        </div>
        <div>
          <input
            type="password"
            placeholder="Confirm Password"
            name="password2"
            value={password2}
            onChange={onChange}
            minLength="8"
            required
          />
        </div>
        <button type="submit">Register</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
}

export default Register;
