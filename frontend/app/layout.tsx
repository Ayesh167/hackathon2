import './globals.css';
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import Navbar from '@/components/Navbar';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Todo App | Manage Your Tasks',
  description: 'A full-featured todo application with authentication and task management',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="min-h-screen flex flex-col">
          <Navbar />
          <main className="flex-grow">
            {children}
          </main>
          <footer className="bg-gray-800 text-white py-6">
            <div className="max-w-4xl mx-auto px-4 text-center">
              <p>© {new Date().getFullYear()} Todo App. All rights reserved.</p>
            </div>
          </footer>
        </div>
      </body>
    </html>
  );
}