import axios from 'axios';

const api = axios.create({
  // When running in Docker, the frontend will connect to the backend
  // using the service name 'backend' as the hostname.
   baseURL: 'http://localhost:8000', // <-- CHANGE THIS BACK
});

// This automatically adds the authentication token to every request
api.interceptors.request.use(config => {
  const token = localStorage.getItem('authToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;