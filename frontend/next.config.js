/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone', // для лучшей производительности
  experimental: {
    serverComponentsExternalPackages: ['@prisma/client'],
  },
  images: {
    domains: ['localhost', 'car-advisor-api.vercel.app'],
  },
  // Удали rewrites для production
  async rewrites() {
    // Проверяем, является ли среда development (по наличию переменной NEXT_PUBLIC_BACKEND_URL или другой индикации)
    const isDevelopment = !process.env.RAILWAY || process.env.NODE_ENV === 'development';

    if (isDevelopment) {
      return [
        {
          source: '/api/:path*',
          destination: `${process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000'}/api/:path*`,
        },
      ];
    }
    // В production оставляем пустой массив rewrites
    return [];
  },
};

module.exports = nextConfig;