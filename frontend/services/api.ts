import axios from 'axios';

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL;
const API_URL = process.env.NEXT_PUBLIC_API_URL;

const API_BASE_URL = BACKEND_URL || API_URL || 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add token to headers and adjust URL
apiClient.interceptors.request.use(
  (config) => {
    // Add /api/v1 prefix to all requests if not already present
    if (!config.url?.startsWith('/api/v1')) {
      config.url = `/api/v1${config.url}`;
    }

    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    console.log(`➡️ Отправляю запрос: ${config.method?.toUpperCase()} ${config.baseURL}${config.url}`);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle token expiration
apiClient.interceptors.response.use(
  (response) => {
    console.log(`✅ Получен ответ: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error(`❌ Ошибка запроса:`, error);
    if (error.response?.status === 401) {
      // Token might be expired, redirect to login
      localStorage.removeItem('token');
      if (typeof window !== 'undefined') {
        window.location.href = '/auth/login';
      }
    }
    return Promise.reject(error);
  }
);

// Экспортируем как default
export default apiClient;