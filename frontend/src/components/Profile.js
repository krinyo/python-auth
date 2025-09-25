import React, { useContext, useState, useEffect } from 'react';
import AuthContext from '../context/AuthContext';
import axiosInstance from '../utils/axiosInstance';

function Profile() {
  const { user, authTokens } = useContext(AuthContext);
  const [profileData, setProfileData] = useState(null);
  const [error, setError] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({});

  const fetchProfile = async () => {
    try {
      const res = await axiosInstance.get('/auth/profile/');
      setProfileData(res.data);
      setFormData(res.data); // Initialize form data
    } catch (err) {
      setError('Failed to fetch profile data.');
      console.error(err);
    }
  };

  useEffect(() => {
    if (user) {
      fetchProfile();
    }
  }, [user, authTokens]);

  const handleEditToggle = () => {
    setIsEditing(!isEditing);
    // Reset form data to profile data on cancel
    if (isEditing) {
      setFormData(profileData);
    }
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSave = async () => {
    try {
      // Only send editable fields
      const dataToSave = {
        first_name: formData.first_name,
        last_name: formData.last_name,
      };
      const res = await axiosInstance.patch('/auth/profile/', dataToSave);
      setProfileData(res.data);
      setIsEditing(false);
      setError(null);
    } catch (err) {
      setError('Failed to update profile.');
      console.error(err.response.data);
    }
  };

  if (!user) {
    return <h2>Please log in to view your profile.</h2>;
  }

  if (error && !isEditing) { // Only show main error when not in edit mode
    return <h2>{error}</h2>;
  }

  if (!profileData) {
    return <h2>Loading profile...</h2>;
  }

  return (
    <div>
      <h2>Profile</h2>
      {isEditing ? (
        <div>
          <div>
            <label>Email: </label>
            <input type="email" name="email" value={formData.email || ''} disabled />
          </div>
          <div>
            <label>First Name: </label>
            <input type="text" name="first_name" value={formData.first_name || ''} onChange={handleChange} />
          </div>
          <div>
            <label>Last Name: </label>
            <input type="text" name="last_name" value={formData.last_name || ''} onChange={handleChange} />
          </div>
          <button onClick={handleSave}>Save</button>
          <button onClick={handleEditToggle}>Cancel</button>
          {error && <p style={{color: 'red'}}>{error}</p>}
        </div>
      ) : (
        <div>
          <p><strong>Email:</strong> {profileData.email}</p>
          <p><strong>First Name:</strong> {profileData.first_name}</p>
          <p><strong>Last Name:</strong> {profileData.last_name}</p>
          <p><strong>Role:</strong> {profileData.role_name}</p>
          <button onClick={handleEditToggle}>Edit</button>
        </div>
      )}
    </div>
  );
}

export default Profile;
