import { useMutation, useQueryClient } from '@tanstack/react-query';
import { authService, LoginCredentials, RegisterData } from '@/services/authService';

export const useLogin = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ email, password }: LoginCredentials) => 
      authService.login({ email, password }),
    onSuccess: (data) => {
      // Store token in localStorage or cookie
      localStorage.setItem('token', data.access_token);
      // Update auth store
      // Note: In a real app, you'd dispatch an action to update the auth store
    },
  });
};

export const useRegister = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ name, email, password }: RegisterData) =>
      authService.register({ name, email, password }),
    onSuccess: (data) => {
      // Store token in localStorage or cookie
      localStorage.setItem('token', data.access_token);
      // Update auth store
      // Note: In a real app, you'd dispatch an action to update the auth store
    },
  });
};

export const useLogout = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: authService.logout,
    onSuccess: () => {
      // Remove token from localStorage or cookie
      localStorage.removeItem('token');
      // Update auth store
      // Note: In a real app, you'd dispatch an action to update the auth store
    },
  });
};