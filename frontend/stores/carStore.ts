import { create } from 'zustand';
import apiClient from '../services/api';

export interface Car {
  id: number;
  make: string;
  model: string;
  year: number;
  price: number;
  description: string;
  features: string[];
}

interface CarState {
  cars: Car[];
  selectedCar: Car | null;
  loading: boolean;
  error: string | null;
  fetchCars: () => Promise<void>;
  fetchCarById: (id: number) => Promise<void>;
  createCar: (carData: Omit<Car, 'id'>) => Promise<void>;
  updateCar: (id: number, carData: Partial<Car>) => Promise<void>;
  deleteCar: (id: number) => Promise<void>;
  setSelectedCar: (car: Car | null) => void;
}

export const useCarStore = create<CarState>((set, get) => ({
  cars: [],
  selectedCar: null,
  loading: false,
  error: null,
  
  fetchCars: async () => {
    set({ loading: true, error: null });
    try {
      const response = await apiClient.get('/cars/');
      set({ cars: response.data, loading: false });
    } catch (error: any) {
      set({ error: error.response?.data?.detail || 'Failed to fetch cars', loading: false });
    }
  },
  
  fetchCarById: async (id) => {
    set({ loading: true, error: null });
    try {
      const response = await apiClient.get(`/cars/${id}`);
      set({ selectedCar: response.data, loading: false });
    } catch (error: any) {
      set({ error: error.response?.data?.detail || 'Failed to fetch car', loading: false });
    }
  },
  
  createCar: async (carData) => {
    set({ loading: true, error: null });
    try {
      const response = await apiClient.post('/cars/', carData);
      const newCar = response.data;
      set(state => ({
        cars: [...state.cars, newCar],
        loading: false
      }));
    } catch (error: any) {
      set({ error: error.response?.data?.detail || 'Failed to create car', loading: false });
    }
  },
  
  updateCar: async (id, carData) => {
    set({ loading: true, error: null });
    try {
      const response = await apiClient.put(`/cars/${id}`, carData);
      const updatedCar = response.data;
      set(state => ({
        cars: state.cars.map(car => car.id === id ? updatedCar : car),
        selectedCar: state.selectedCar?.id === id ? updatedCar : state.selectedCar,
        loading: false
      }));
    } catch (error: any) {
      set({ error: error.response?.data?.detail || 'Failed to update car', loading: false });
    }
  },
  
  deleteCar: async (id) => {
    set({ loading: true, error: null });
    try {
      await apiClient.delete(`/cars/${id}`);
      set(state => ({
        cars: state.cars.filter(car => car.id !== id),
        selectedCar: state.selectedCar?.id === id ? null : state.selectedCar,
        loading: false
      }));
    } catch (error: any) {
      set({ error: error.response?.data?.detail || 'Failed to delete car', loading: false });
    }
  },
  
  setSelectedCar: (car) => set({ selectedCar: car }),
}));