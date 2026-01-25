'use client';

import { apiClient } from '@/services/api';

const TestConnection = () => {
  const testBackend = async () => {
    console.log('🔍 Тестирую подключение к бэкенду...');
    
    try {
      // 1. Проверяем доступность бэкенда
      console.log('API Client baseURL:', apiClient.defaults.baseURL);
      
      // 2. Пробуем сделать пробный запрос
      const response = await apiClient.get('/health');
      console.log('✅ Health check:', response.data);
      
    } catch (error: any) {
      console.error('❌ Ошибка теста:', {
        url: error.config?.url,
        baseURL: error.config?.baseURL,
        fullUrl: error.config?.baseURL + error.config?.url,
        message: error.message,
        response: error.response,
      });
    }
  };
  
  return (
    <button 
      onClick={testBackend}
      className="p-2 bg-blue-500 text-white rounded m-4"
    >
      Тест подключения к бэкенду
    </button>
  );
};

export default TestConnection;