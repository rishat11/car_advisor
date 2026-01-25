'use client';

import { useState } from 'react';
import { useCars, useCreateCar, useUpdateCar, useDeleteCar } from '@/hooks/useCars';
import CarCard from '@/components/CarCard';
import CarForm from '@/components/CarForm';
import { motion } from 'framer-motion';
import ProtectedRoute from '@/components/ProtectedRoute';

export default function CarsPage() {
  const { data: cars = [], isLoading, error, refetch } = useCars();
  const createCarMutation = useCreateCar();
  const updateCarMutation = useUpdateCar();
  const deleteCarMutation = useDeleteCar();
  
  const [showForm, setShowForm] = useState(false);
  const [editingCar, setEditingCar] = useState<any>(null);

  const handleCreateCar = async (data: any) => {
    try {
      await createCarMutation.mutateAsync(data);
      setShowForm(false);
    } catch (err) {
      console.error('Error creating car:', err);
    }
  };

  const handleUpdateCar = async (data: any) => {
    if (editingCar) {
      try {
        await updateCarMutation.mutateAsync({ id: editingCar.id, data });
        setEditingCar(null);
        setShowForm(false);
      } catch (err) {
        console.error('Error updating car:', err);
      }
    }
  };

  const handleDeleteCar = async (id: number) => {
    if (confirm('Are you sure you want to delete this car?')) {
      try {
        await deleteCarMutation.mutateAsync(id);
      } catch (err) {
        console.error('Error deleting car:', err);
      }
    }
  };

  const handleEditCar = (car: any) => {
    setEditingCar(car);
    setShowForm(true);
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading cars...</p>
        </div>
      </div>
    );
  }

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gray-50">
        <header className="bg-white shadow">
          <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8 flex justify-between items-center">
            <h1 className="text-2xl font-bold text-gray-900">Car Inventory</h1>
            <button
              onClick={() => {
                setEditingCar(null);
                setShowForm(true);
              }}
              className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              Add Car
            </button>
          </div>
        </header>

        <main className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
          {error && (
            <div className="rounded-md bg-red-50 p-4 mb-6">
              <div className="text-sm text-red-700">{(error as Error).message}</div>
            </div>
          )}

          {showForm ? (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="mb-8"
            >
              <CarForm
                car={editingCar}
                onSubmit={editingCar ? handleUpdateCar : handleCreateCar}
                onCancel={() => {
                  setShowForm(false);
                  setEditingCar(null);
                }}
                submitText={editingCar ? 'Update Car' : 'Create Car'}
              />
            </motion.div>
          ) : null}

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {cars.map((car) => (
              <CarCard 
                key={car.id} 
                car={car} 
                onDelete={handleDeleteCar} 
              />
            ))}
          </div>

          {cars.length === 0 && !showForm && (
            <div className="text-center py-12">
              <p className="text-gray-500">No cars found. Add your first car to get started.</p>
            </div>
          )}
        </main>
      </div>
    </ProtectedRoute>
  );
}