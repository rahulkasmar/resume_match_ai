import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000', // Your FastAPI server URL
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