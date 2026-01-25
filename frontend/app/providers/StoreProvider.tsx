// app/providers/StoreProvider.tsx
'use client';

import { PropsWithChildren } from 'react';
import { useAuthStore } from '@/stores/authStore';

export default function StoreProvider({ children }: PropsWithChildren) {
  // Initialize auth store on client side
  useAuthStore();

  return <>{children}</>;
}