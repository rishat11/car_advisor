import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { usePathname } from 'next/navigation';
import { useAuthStore } from '@/stores/authStore';

export const useAuth = () => {
  const router = useRouter();
  const pathname = usePathname();
  const { isAuthenticated, verifyToken } = useAuthStore();

  useEffect(() => {
    const checkAuth = async () => {
      const isValid = await verifyToken();
      if (!isValid && !['/auth/login', '/auth/register'].includes(pathname)) {
        router.push('/auth/login');
      }
    };

    checkAuth();
  }, [router, pathname, verifyToken]);

  return { isAuthenticated };
};