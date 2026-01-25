// Define common types for the application

export interface User {
  id: number;
  email: string;
  name: string;
}

export interface Car {
  id: number;
  make: string;
  model: string;
  year: number;
  price: number;
  description: string;
  features: string[];
}

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}