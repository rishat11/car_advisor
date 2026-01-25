import apiClient from './api';

interface ChatMessageRequest {
  message: string;
}

interface ChatMessageResponse {
  response: string;
}

export const chatService = {
  sendMessage: async (request: ChatMessageRequest): Promise<ChatMessageResponse> => {
    const response = await apiClient.post('/chat/', request);
    return response.data;
  },
};