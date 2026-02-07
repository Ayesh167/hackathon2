'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { apiClient } from '../lib/api';

const Navbar = () => {
  const router = useRouter();
  const pathname = usePathname();
  const [userName, setUserName] = useState<string | null>(null);

  useEffect(() => {
    // Get user info from localStorage or API
    // For now, we'll extract from token or use mock data
    const token = localStorage.getItem('jwt_token');
    if (token) {
      // In a real app, we would decode the JWT or fetch user info
      // For now, we'll use mock data
      setUserName('User');
    } else {
      setUserName(null);
    }
  }, []);

  const handleLogout = async () => {
    // Clear the token from localStorage
    apiClient.logout();

    // Redirect to login page
    router.push('/login');
    router.refresh(); // Refresh to update the navbar
  };

  // Don't show navbar on login/signup pages
  if (pathname === '/login' || pathname === '/signup') {
    return null;
  }

  return (
    <nav className="bg-blue-600 text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center">
            <Link href="/tasks" className="text-xl font-bold flex items-center">
              <span className="mr-2">📋</span>
              <span>Todo App</span>
            </Link>
          </div>

          <div className="flex items-center">
            {userName && (
              <div className="hidden md:block mr-6 text-sm">
                Welcome, <span className="font-semibold">{userName}</span>
              </div>
            )}

            <div className="flex items-center space-x-4">
              <Link
                href="/tasks"
                className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  pathname === '/tasks'
                    ? 'bg-blue-700 text-white'
                    : 'text-blue-100 hover:bg-blue-700 hover:text-white'
                }`}
              >
                My Tasks
              </Link>

              <Link
                href="/chat"
                className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  pathname === '/chat'
                    ? 'bg-blue-700 text-white'
                    : 'text-blue-100 hover:bg-blue-700 hover:text-white'
                }`}
              >
                AI Assistant
              </Link>

              <Link
                href="/profile"
                className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  pathname === '/profile'
                    ? 'bg-blue-700 text-white'
                    : 'text-blue-100 hover:bg-blue-700 hover:text-white'
                }`}
              >
                Profile
              </Link>

              <button
                onClick={handleLogout}
                className="ml-2 px-3 py-2 bg-blue-700 hover:bg-blue-800 rounded-md text-sm font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-blue-300"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;