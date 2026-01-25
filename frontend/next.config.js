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
    if (process.env.NODE_ENV === 'development') {
      return [
        {
          source: '/api/:path*',
          destination: 'http://localhost:8000/api/:path*',
        },
      ];
    }
    return [];
  },
};

module.exports = nextConfig;