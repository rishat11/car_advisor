import { create } from 'zustand';
import apiClient from '../services/api';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

interface ChatState {
  messages: Message[];
  isLoading: boolean;
  error: string | null;
  sendMessage: (message: string) => Promise<void>;
  resetChat: () => void;
  initializeChat: () => void;
}

export const useChatStore = create<ChatState>((set, get) => ({
  messages: [],
  isLoading: false,
  error: null,
  
  initializeChat: () => {
    set({
      messages: [
        {
          id: '1',
          role: 'assistant',
          content: 'Привет! Я ваш AI помощник по автомобилям. Спросите меня о рекомендациях, характеристиках или сравнении автомобилей.',
          timestamp: new Date(),
        }
      ],
      isLoading: false,
      error: null,
    });
  },
  
  sendMessage: async (message) => {
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: message,
      timestamp: new Date(),
    };
    
    set((state) => ({
      messages: [...state.messages, userMessage],
      isLoading: true,
      error: null,
    }));
    
    try {
      const response = await apiClient.post('/chat/', { message });
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.data.response,
        timestamp: new Date(),
      };

      set((state) => ({
        messages: [...state.messages, aiMessage],
        isLoading: false,
      }));
    } catch (error: any) {
      set({
        error: error.response?.data?.detail || 'Failed to send message',
        isLoading: false,
      });
    }
  },
  
  resetChat: () => {
    set({
      messages: [
        {
          id: '1',
          role: 'assistant',
          content: 'Привет! Я ваш AI помощник по автомобилям. Спросите меня о рекомендациях, характеристиках или сравнении автомобилей.',
          timestamp: new Date(),
        }
      ],
      isLoading: false,
      error: null,
    });
  },
}));