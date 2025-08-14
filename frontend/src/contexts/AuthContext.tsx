import { createContext, useState, type ReactNode } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../lib/api';

// ... (interface AuthContextType stays the same, but add signup)
interface AuthContextType {
  token: string | null;
  login: (data: FormData) => Promise<void>;
  signup: (data: any) => Promise<void>; // Added signup
  logout: () => void;
}

export const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string | null>(localStorage.getItem('authToken'));
  const navigate = useNavigate();

  const login = async (formData: FormData) => {
    const response = await api.post('/auth/login', formData);
    const newToken = response.data.access_token;
    setToken(newToken);
    localStorage.setItem('authToken', newToken);
  };

  const signup = async (userData: any) => {
    await api.post('/auth/signup', userData);
  };

  const logout = () => {
    setToken(null);
    localStorage.removeItem('authToken');
    navigate('/login');
  };

  const value = { token, login, signup, logout };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}