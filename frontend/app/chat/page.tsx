'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { apiClient } from '@/lib/api';
import ChatInterface from '@/components/chat/ChatInterface';

const ChatPage = () => {
  const router = useRouter();
  const [userId, setUserId] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);

  // Check if user is authenticated by trying to get user details
  useEffect(() => {
    const checkAuth = async () => {
      try {
        const response = await apiClient.getUserDetails();
        if (response.data) {
          setIsAuthenticated(true);
          setUserId(response.data.id);
        } else {
          setIsAuthenticated(false);
          router.push('/login');
        }
      } catch (error) {
        console.error('Authentication check failed:', error);
        setIsAuthenticated(false);
        router.push('/login');
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, [router]);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="text-xl">Loading...</div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null; // Redirect handled by useEffect
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-800 mb-6">AI Task Assistant</h1>
      <p className="text-gray-600 mb-8">
        Chat with our AI assistant to manage your tasks using natural language.
      </p>
      
      <div className="bg-white rounded-lg shadow-lg p-6">
        {userId ? (
          <ChatInterface userId={userId} />
        ) : (
          <div className="text-center text-gray-500">
            Loading user information...
          </div>
        )}
      </div>
      
      <div className="mt-8 text-sm text-gray-500">
        <p>Examples of what you can say:</p>
        <ul className="list-disc pl-5 mt-2 space-y-1">
          <li>"Create a task to buy groceries"</li>
          <li>"Show me my pending tasks"</li>
          <li>"Mark the meeting task as complete"</li>
          <li>"Update my project deadline to next week"</li>
        </ul>
      </div>
    </div>
  );
};

export default ChatPage;