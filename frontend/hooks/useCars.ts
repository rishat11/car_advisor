import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { carService, Car, CreateCarData, UpdateCarData } from '@/services/carService';

export const useCars = () => {
  return useQuery<Car[], Error>({
    queryKey: ['cars'],
    queryFn: carService.getAll,
  });
};

export const useCar = (id: number) => {
  return useQuery<Car, Error>({
    queryKey: ['cars', id],
    queryFn: () => carService.getById(id),
    enabled: !!id,
  });
};

export const useCreateCar = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (carData: CreateCarData) => carService.create(carData),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['cars'] });
    },
  });
};

export const useUpdateCar = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: UpdateCarData }) => 
      carService.update(id, data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['cars'] });
      queryClient.invalidateQueries({ queryKey: ['cars', variables.id] });
    },
  });
};

export const useDeleteCar = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (id: number) => carService.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['cars'] });
    },
  });
};