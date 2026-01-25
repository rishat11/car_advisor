# Car Advisor Frontend

A production-ready React/Next.js frontend for the Car Advisor application with AI-powered car recommendations.

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **Server State**: React Query (TanStack Query)
- **HTTP Client**: Axios
- **Animations**: Framer Motion
- **Forms**: React Hook Form + Zod for validation

## Features

1. **Authentication System**
   - User registration and login
   - Protected routes
   - JWT token management

2. **Car Management (CRUD)**
   - Create, read, update, and delete cars
   - Car listings with filtering and search
   - Detailed car views

3. **AI Chat Assistant**
   - Real-time conversation with AI
   - Car recommendation engine
   - Context-aware responses

## Setup Instructions

1. Install dependencies:
```bash
npm install
```

2. Create a `.env.local` file in the root directory with the following:
```env
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

For Docker environments, the `NEXT_PUBLIC_DOCKER_ENVIRONMENT` variable will be set automatically to ensure API requests go through the Next.js proxy.

3. Run the development server:
```bash
npm run dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser

## Project Structure

```
app/
├── auth/
│   ├── login/
│   └── register/
├── dashboard/
├── cars/
├── chat/
├── profile/
components/
├── AuthForm.tsx
├── CarCard.tsx
├── CarForm.tsx
├── ChatComponent.tsx
├── ProtectedRoute.tsx
hooks/
├── useAuth.ts
├── useCars.ts
├── useChat.ts
├── useAuthApi.ts
services/
├── api.ts
├── authService.ts
├── carService.ts
├── chatService.ts
stores/
├── authStore.ts
├── carStore.ts
├── chatStore.ts
types/
utils/
```

## Key Components

- **AuthForm**: Handles user registration and login
- **CarCard**: Displays individual car information
- **CarForm**: Handles car creation and editing
- **ChatComponent**: Provides AI chat interface
- **ProtectedRoute**: Wrapper for authenticated routes

## API Integration

The frontend integrates with the FastAPI backend through the following endpoints:

- `/api/v1/auth/*` - Authentication endpoints
- `/api/v1/cars/*` - Car management endpoints
- `/api/v1/chat/*` - AI chat endpoints

The Next.js proxy configuration in `next.config.js` forwards API requests to the backend server running on port 8000.

## State Management

- **Zustand**: Used for global state management (authentication, cars, chat)
- **React Query**: Used for server state management and caching API responses

## Security

- Protected routes using middleware and custom components
- JWT token stored in localStorage with automatic refresh
- Input validation using Zod schemas
- Secure HTTP headers configuration

## Performance

- Client-side rendering with Next.js App Router
- Server state caching with React Query
- Component lazy loading
- Image optimization
- Bundle size optimization