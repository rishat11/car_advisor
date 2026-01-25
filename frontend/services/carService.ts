import apiClient from './api';

export interface Car {
  id: number;
  make: string;
  model: string;
  year: number;
  price: number;
  description: string;
  features: string[];
}

export interface CreateCarData {
  make: string;
  model: string;
  year: number;
  price: number;
  description: string;
  features: string[];
}

export interface UpdateCarData {
  make?: string;
  model?: string;
  year?: number;
  price?: number;
  description?: string;
  features?: string[];
}

export const carService = {
  getAll: async (): Promise<Car[]> => {
    const response = await apiClient.get('/cars/');
    return response.data;
  },

  getById: async (id: number): Promise<Car> => {
    const response = await apiClient.get(`/cars/${id}`);
    return response.data;
  },

  create: async (data: CreateCarData): Promise<Car> => {
    const response = await apiClient.post('/cars/', data);
    return response.data;
  },

  update: async (id: number, data: UpdateCarData): Promise<Car> => {
    const response = await apiClient.put(`/cars/${id}`, data);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await apiClient.delete(`/cars/${id}`);
  },
};