import apiClient from './api';

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  name: string;
  email: string;
  password: string;
}

interface User {
  id: number;
  email: string;
  name: string;
}

export const authService = {
  login: async (credentials: LoginCredentials) => {
    const response = await apiClient.post('/login', credentials);
    return response.data;
  },

  register: async (userData: RegisterData) => {
    // Map frontend fields to backend fields
    const requestData = {
      name: userData.name,
      email: userData.email,
      password: userData.password
    };
    const response = await apiClient.post('/register', requestData);
    return response.data;
  },

  logout: async () => {
    // In a real app, you might want to call a backend endpoint to invalidate the token
    return Promise.resolve();
  },

  getCurrentUser: async () => {
    const response = await apiClient.get('/me');
    return response.data as User;
  },
};