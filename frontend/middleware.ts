import { NextRequest, NextResponse } from 'next/server';
import { jwtVerify } from 'jose';

const protectedPaths = ['/dashboard', '/cars', '/chat', '/profile'];

export async function middleware(request: NextRequest) {
  // Check if the path is protected
  const isProtectedPath = protectedPaths.some(path => 
    request.nextUrl.pathname.startsWith(path)
  );

  if (!isProtectedPath) {
    return NextResponse.next();
  }

  // In a real application, you would verify the JWT token here
  // For now, we'll just check if there's a token in cookies/localStorage
  // Since we can't access browser storage from server-side middleware,
  // we'll skip this implementation for now and handle auth in components
  
  return NextResponse.next();
}

export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
}