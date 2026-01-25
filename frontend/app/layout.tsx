import './globals.css'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import QueryProvider from './providers/QueryProvider'
import StoreProvider from './providers/StoreProvider'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Car Advisor',
  description: 'AI-powered car recommendation system',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <QueryProvider>
          <StoreProvider>
            {children}
          </StoreProvider>
        </QueryProvider>
      </body>
    </html>
  )
}