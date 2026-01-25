'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/stores/authStore';
import { motion } from 'framer-motion';
import Link from 'next/link';
import ProtectedRoute from '@/components/ProtectedRoute';

export default function DashboardPage() {
  const router = useRouter();
  const { isAuthenticated, user, logout } = useAuthStore();

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/auth/login');
    }
  }, [isAuthenticated, router]);

  if (!isAuthenticated) {
    return null; // Render nothing while redirecting
  }

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gray-50">
        <header className="bg-white shadow">
          <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8 flex justify-between items-center">
            <h1 className="text-2xl font-bold text-gray-900">Car Advisor Dashboard</h1>
            <div className="flex items-center space-x-4">
              <span className="text-gray-700">Welcome, {user?.name || user?.email}</span>
              <button
                onClick={logout}
                className="ml-4 px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
              >
                Logout
              </button>
            </div>
          </div>
        </header>

        <main className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <motion.div 
              whileHover={{ scale: 1.03 }}
              className="bg-white p-6 rounded-lg shadow-md"
            >
              <h2 className="text-xl font-semibold text-gray-800 mb-4">Manage Cars</h2>
              <p className="text-gray-600 mb-4">View, add, edit, and delete cars in your inventory</p>
              <Link 
                href="/cars"
                className="inline-block px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700"
              >
                Manage Cars
              </Link>
            </motion.div>

            <motion.div 
              whileHover={{ scale: 1.03 }}
              className="bg-white p-6 rounded-lg shadow-md"
            >
              <h2 className="text-xl font-semibold text-gray-800 mb-4">AI Car Advisor</h2>
              <p className="text-gray-600 mb-4">Get recommendations and advice from our AI assistant</p>
              <Link 
                href="/chat"
                className="inline-block px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700"
              >
                Start Chatting
              </Link>
            </motion.div>

            <motion.div 
              whileHover={{ scale: 1.03 }}
              className="bg-white p-6 rounded-lg shadow-md"
            >
              <h2 className="text-xl font-semibold text-gray-800 mb-4">Profile Settings</h2>
              <p className="text-gray-600 mb-4">Update your account information</p>
              <Link 
                href="/profile"
                className="inline-block px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700"
              >
                Manage Profile
              </Link>
            </motion.div>
          </div>
        </main>
      </div>
    </ProtectedRoute>
  );
}