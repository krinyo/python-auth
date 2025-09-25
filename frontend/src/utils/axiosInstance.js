import axios from 'axios';

const axiosInstance = axios.create({
    baseURL: '/api',
    headers: {
        'Content-Type': 'application/json'
    }
});

// Request interceptor to add the token
axiosInstance.interceptors.request.use(
    config => {
        const tokens = localStorage.getItem('authTokens') ? JSON.parse(localStorage.getItem('authTokens')) : null;
        if (tokens) {
            config.headers.Authorization = `Bearer ${tokens.access}`;
        }
        return config;
    },
    error => Promise.reject(error)
);

// Response interceptor to handle 401 and refresh token
axiosInstance.interceptors.response.use(
    response => response,
    async error => {
        const originalRequest = error.config;

        // Check if the error is 401 and it's not a retry request
        if (error.response.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            const tokens = localStorage.getItem('authTokens') ? JSON.parse(localStorage.getItem('authTokens')) : null;

            if (tokens?.refresh) {
                try {
                    const response = await axios.post('/api/token/refresh/', {
                        refresh: tokens.refresh
                    });

                    const newTokens = response.data;
                    localStorage.setItem('authTokens', JSON.stringify(newTokens));

                    // Update the header for the original request
                    axiosInstance.defaults.headers.common['Authorization'] = `Bearer ${newTokens.access}`;
                    originalRequest.headers['Authorization'] = `Bearer ${newTokens.access}`;

                    return axiosInstance(originalRequest);
                } catch (refreshError) {
                    // If refresh fails, clear tokens and redirect to login
                    localStorage.removeItem('authTokens');
                    delete axiosInstance.defaults.headers.common['Authorization'];
                    // This is tricky, we can't easily redirect from here.
                    // The AuthContext should handle the logout.
                    // We'll just reject the promise.
                    console.error("Token refresh failed", refreshError);
                    window.location.href = '/login'; // Force redirect
                    return Promise.reject(refreshError);
                }
            }
        }

        return Promise.reject(error);
    }
);

export default axiosInstance;
