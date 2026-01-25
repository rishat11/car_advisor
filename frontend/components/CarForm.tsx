'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { motion } from 'framer-motion';
import { Car } from '@/stores/carStore';

const carSchema = z.object({
  make: z.string().min(1, 'Make is required'),
  model: z.string().min(1, 'Model is required'),
  year: z.number().min(1900).max(new Date().getFullYear() + 1),
  price: z.number().positive('Price must be positive'),
  description: z.string().min(1, 'Description is required'),
  features: z.string().transform(str => str.split(',').map(s => s.trim())),
});

// The form will work with the raw (non-transformed) values
type RawCarFormData = {
  make: string;
  model: string;
  year: number;
  price: number;
  description: string;
  features: string; // Form field expects string
};

// The transformed data type that will be returned after schema processing
type TransformedCarFormData = z.infer<typeof carSchema>; // This will have features as string[]

interface CarFormProps {
  car?: Car;
  onSubmit: (data: TransformedCarFormData) => void;
  onCancel: () => void;
  submitText?: string;
}

export default function CarForm({ car, onSubmit, onCancel, submitText = 'Save Car' }: CarFormProps) {
  const [error, setError] = useState<string | null>(null);
  
  const {
    register,
    handleSubmit,
    formState: { errors },
    setValue,
  } = useForm<RawCarFormData>({
    resolver: zodResolver(carSchema),
    defaultValues: car
      ? {
          make: car.make,
          model: car.model,
          year: car.year,
          price: car.price,
          description: car.description,
          features: car.features.join(', '), // Convert array back to comma-separated string
        }
      : {
          make: '',
          model: '',
          year: new Date().getFullYear(),
          price: 0,
          description: '',
          features: '',
        },
  });

  const onSubmitHandler = (data: RawCarFormData) => {
    try {
      // Transform the raw form data using the schema
      const transformedData = carSchema.parse(data);
      onSubmit(transformedData);
    } catch (err: any) {
      setError(err.message || 'An error occurred');
    }
  };

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="w-full max-w-2xl p-6 bg-white rounded-xl shadow-lg"
    >
      <h2 className="text-2xl font-bold text-gray-900 mb-6">
        {car ? 'Edit Car' : 'Add New Car'}
      </h2>
      
      {error && (
        <div className="rounded-md bg-red-50 p-4 mb-4">
          <div className="text-sm text-red-700">{error}</div>
        </div>
      )}
      
      <form onSubmit={handleSubmit(onSubmitHandler)} className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label htmlFor="make" className="block text-sm font-medium text-gray-700">
              Make
            </label>
            <input
              id="make"
              type="text"
              {...register('make', { valueAsNumber: false })}
              className={`mt-1 block w-full px-3 py-2 border ${
                errors.make ? 'border-red-500' : 'border-gray-300'
              } rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500`}
            />
            {errors.make && errors.make.message && (
              <p className="mt-1 text-sm text-red-600">{errors.make.message?.toString()}</p>
            )}
          </div>
          
          <div>
            <label htmlFor="model" className="block text-sm font-medium text-gray-700">
              Model
            </label>
            <input
              id="model"
              type="text"
              {...register('model', { valueAsNumber: false })}
              className={`mt-1 block w-full px-3 py-2 border ${
                errors.model ? 'border-red-500' : 'border-gray-300'
              } rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500`}
            />
            {errors.model && errors.model.message && (
              <p className="mt-1 text-sm text-red-600">{errors.model.message?.toString()}</p>
            )}
          </div>
          
          <div>
            <label htmlFor="year" className="block text-sm font-medium text-gray-700">
              Year
            </label>
            <input
              id="year"
              type="number"
              {...register('year', { valueAsNumber: true })}
              className={`mt-1 block w-full px-3 py-2 border ${
                errors.year ? 'border-red-500' : 'border-gray-300'
              } rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500`}
            />
            {errors.year && errors.year.message && (
              <p className="mt-1 text-sm text-red-600">{errors.year.message?.toString()}</p>
            )}
          </div>
          
          <div>
            <label htmlFor="price" className="block text-sm font-medium text-gray-700">
              Price ($)
            </label>
            <input
              id="price"
              type="number"
              step="0.01"
              {...register('price', { valueAsNumber: true })}
              className={`mt-1 block w-full px-3 py-2 border ${
                errors.price ? 'border-red-500' : 'border-gray-300'
              } rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500`}
            />
            {errors.price && errors.price.message && (
              <p className="mt-1 text-sm text-red-600">{errors.price.message?.toString()}</p>
            )}
          </div>
        </div>
        
        <div>
          <label htmlFor="description" className="block text-sm font-medium text-gray-700">
            Description
          </label>
          <textarea
            id="description"
            rows={4}
            {...register('description')}
            className={`mt-1 block w-full px-3 py-2 border ${
              errors.description ? 'border-red-500' : 'border-gray-300'
            } rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500`}
          />
          {errors.description && errors.description.message && (
            <p className="mt-1 text-sm text-red-600">{errors.description.message?.toString()}</p>
          )}
        </div>
        
        <div>
          <label htmlFor="features" className="block text-sm font-medium text-gray-700">
            Features (comma separated)
          </label>
          <textarea
            id="features"
            rows={2}
            placeholder="Feature 1, Feature 2, Feature 3..."
            {...register('features')}
            className={`mt-1 block w-full px-3 py-2 border ${
              errors.features ? 'border-red-500' : 'border-gray-300'
            } rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500`}
          />
          {errors.features && errors.features.message && (
            <p className="mt-1 text-sm text-red-600">{errors.features.message?.toString()}</p>
          )}
        </div>
        
        <div className="flex justify-end space-x-3 pt-4">
          <button
            type="button"
            onClick={onCancel}
            className="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
          >
            Cancel
          </button>
          <button
            type="submit"
            className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
          >
            {submitText}
          </button>
        </div>
      </form>
    </motion.div>
  );
}