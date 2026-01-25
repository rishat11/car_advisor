import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import apiClient from '../services/api';

interface AuthState {
  user: any | null;
  token: string | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, name: string) => Promise<void>;
  logout: () => void;
  verifyToken: () => Promise<boolean>;
  updateProfile: (name: string, email: string) => Promise<void>;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      
      login: async (email, password) => {
        try {
          const response = await apiClient.post('/auth/login', { email, password });
          const { access_token, user } = response.data;

          // Set authorization header for subsequent requests
          apiClient.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;

          set({
            token: access_token,
            user,
            isAuthenticated: true
          });
        } catch (error: any) {
          throw new Error(error.response?.data?.detail || 'Login failed');
        }
      },
      
      register: async (email, password, name) => {
        try {
          const response = await apiClient.post('/auth/register', {
            email,
            password,
            name
          });
          const { access_token, user } = response.data;

          // Set authorization header for subsequent requests
          apiClient.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;

          set({
            token: access_token,
            user,
            isAuthenticated: true
          });
        } catch (error: any) {
          throw new Error(error.response?.data?.detail || 'Registration failed');
        }
      },
      
      logout: () => {
        delete apiClient.defaults.headers.common['Authorization'];
        set({ token: null, user: null, isAuthenticated: false });
      },
      
      verifyToken: async () => {
        const token = get().token;
        if (!token) return false;

        try {
          apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`;
          const response = await apiClient.get('/auth/me');
          set({
            user: response.data,
            isAuthenticated: true
          });
          return true;
        } catch (error) {
          set({ token: null, user: null, isAuthenticated: false });
          return false;
        }
      },

      updateProfile: async (name, email) => {
        try {
          const response = await apiClient.put('/profile', {
            name,
            email
          });

          // Update the user in the store with the response data
          set({
            user: { ...get().user, name, email }, // Update with new values
            isAuthenticated: true
          });

          return response.data;
        } catch (error: any) {
          throw new Error(error.response?.data?.detail || 'Failed to update profile');
        }
      }
    }),
    {
      name: 'auth-storage',
    }
  )
);