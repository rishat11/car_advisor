import { useMutation, useQueryClient } from '@tanstack/react-query';
import { chatService } from '@/services/chatService';

export const useSendMessage = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (message: string) => chatService.sendMessage({ message }),
    onSuccess: () => {
      // Invalidate and refetch chat history if needed
      queryClient.invalidateQueries({ queryKey: ['chat'] });
    },
  });
};