'use client';

import ChatComponent from '@/components/ChatComponent';
import ProtectedRoute from '@/components/ProtectedRoute';

export default function ChatPage() {
  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gray-50">
        <header className="bg-white shadow">
          <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
            <h1 className="text-2xl font-bold text-gray-900">AI Car Advisor Chat</h1>
          </div>
        </header>

        <main className="max-w-4xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
          <div className="h-[600px]">
            <ChatComponent />
          </div>
        </main>
      </div>
    </ProtectedRoute>
  );
}