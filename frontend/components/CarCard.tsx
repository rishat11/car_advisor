'use client';

import { Car } from '@/stores/carStore';
import { motion } from 'framer-motion';
import Link from 'next/link';

interface CarCardProps {
  car: Car;
  onDelete: (id: number) => void;
}

export default function CarCard({ car, onDelete }: CarCardProps) {
  return (
    <motion.div 
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.2 }}
      className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow"
    >
      <div className="p-6">
        <div className="flex justify-between items-start">
          <div>
            <h3 className="text-xl font-bold text-gray-900">{car.make} {car.model}</h3>
            <p className="text-gray-600">{car.year}</p>
          </div>
          <span className="text-lg font-semibold text-primary-600">${car.price.toLocaleString()}</span>
        </div>
        
        <p className="mt-2 text-gray-700 line-clamp-2">{car.description}</p>
        
        <div className="mt-4">
          <h4 className="text-sm font-medium text-gray-900">Features:</h4>
          <ul className="mt-1 grid grid-cols-2 gap-1">
            {car.features.slice(0, 4).map((feature, index) => (
              <li key={index} className="text-xs text-gray-600 flex items-center">
                <span className="mr-1">•</span> {feature}
              </li>
            ))}
            {car.features.length > 4 && (
              <li className="text-xs text-gray-600">+ {car.features.length - 4} more</li>
            )}
          </ul>
        </div>
        
        <div className="mt-6 flex justify-between">
          <Link 
            href={`/cars/${car.id}`}
            className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 transition-colors"
          >
            View Details
          </Link>
          <button
            onClick={() => onDelete(car.id)}
            className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors"
          >
            Delete
          </button>
        </div>
      </div>
    </motion.div>
  );
}