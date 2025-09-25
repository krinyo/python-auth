import React, { useState, useEffect } from 'react';
import axiosInstance from '../utils/axiosInstance';

function TestResource() {
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchResource = async () => {
      try {
        const res = await axiosInstance.get('/auth/test-resource/');
        setMessage(res.data.message);
      } catch (err) {
        if (err.response && err.response.status === 403) {
          setError('Access Denied: You do not have permission to view this resource.');
        } else {
          setError('Failed to fetch the resource.');
        }
        console.error(err);
      }
    };

    fetchResource();
  }, []);

  return (
    <div>
      <h2>Test Resource Page</h2>
      {message && <p style={{ color: 'green' }}>{message}</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {!message && !error && <p>Loading...</p>}
    </div>
  );
}

export default TestResource;
