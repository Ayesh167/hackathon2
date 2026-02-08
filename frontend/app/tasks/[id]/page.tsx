'use client';

import React, { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import TaskForm from '@/components/TaskForm';
import Button from '@/components/Button';
import { apiClient } from '@/lib/api';
import { Task, UpdateTaskData } from '@/lib/types/task';

// Simple function to decode JWT token to get user ID
const getUserIdFromToken = (): string | null => {
  const token = localStorage.getItem('jwt_token');
  if (!token) return null;

  try {
    // Split the token to get the payload part
    const parts = token.split('.');
    if (parts.length !== 3) return null;

    // Decode the payload (second part)
    const payload = parts[1];
    // Add padding if needed
    const paddedPayload = payload + '='.repeat((4 - payload.length % 4) % 4);
    const decodedPayload = atob(paddedPayload);
    const parsedPayload = JSON.parse(decodedPayload);

    // Return the subject (user ID) from the token
    return parsedPayload.sub || null;
  } catch (error) {
    console.error('Error decoding token:', error);
    return null;
  }
};

const TaskDetailPage = () => {
  const { id } = useParams();
  const router = useRouter();
  const [task, setTask] = useState<Task | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [isEditing, setIsEditing] = useState(false);
  const [userId, setUserId] = useState<string | null>(null);

  useEffect(() => {
    const token = localStorage.getItem('jwt_token');
    if (!token) {
      router.push('/login');
      return;
    }

    const extractedUserId = getUserIdFromToken();
    if (!extractedUserId) {
      router.push('/login');
      return;
    }

    setUserId(extractedUserId);
  }, [router]);

  useEffect(() => {
    if (!userId || !id) return;

    const fetchTask = async () => {
      try {
        setLoading(true);
        const response = await apiClient.getTask(userId, id as string);
        
        if (response.error) {
          setError(response.error);
        } else if (response.data) {
          setTask(response.data);
        }
      } catch (err) {
        setError('Failed to load task');
        console.error('Error fetching task:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchTask();
  }, [id, userId]);

  const handleUpdateTask = async (taskData: UpdateTaskData) => {
    if (!task || !userId) return;

    try {
      const response = await apiClient.updateTask(userId, task.id, taskData);

      if (response.error) {
        console.error('Error updating task:', response.error);
      } else if (response.data) {
        setTask(response.data);
        setIsEditing(false);
      }
    } catch (err) {
      console.error('Error updating task:', err);
    }
  };

  const handleDeleteTask = async () => {
    if (!window.confirm('Are you sure you want to delete this task?')) {
      return;
    }

    if (!task || !userId) return;

    try {
      const response = await apiClient.deleteTask(userId, task.id);
      
      if (response.error) {
        console.error('Error deleting task:', response.error);
      } else {
        router.push('/tasks');
      }
    } catch (err) {
      console.error('Error deleting task:', err);
    }
  };

  const handleToggleComplete = async () => {
    if (!task || !userId) return;

    try {
      const response = await apiClient.toggleTaskCompletion(userId, task.id);
      
      if (response.error) {
        console.error('Error toggling task completion:', response.error);
      } else if (response.data) {
        setTask(response.data);
      }
    } catch (err) {
      console.error('Error toggling task completion:', err);
    }
  };

  const handleCancelEdit = () => {
    setIsEditing(false);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading task...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="bg-white rounded-lg shadow-md p-8 max-w-md w-full mx-4">
          <div className="text-center">
            <div className="mx-auto h-16 w-16 bg-red-100 rounded-full flex items-center justify-center mb-4">
              <span className="text-red-600 text-2xl">⚠️</span>
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-1">Error Loading Task</h3>
            <p className="text-gray-500 mb-4">{error}</p>
            <Button 
              variant="primary" 
              size="md"
              onClick={() => router.back()}
            >
              Go Back
            </Button>
          </div>
        </div>
      </div>
    );
  }

  if (!task) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="bg-white rounded-lg shadow-md p-8 max-w-md w-full mx-4">
          <div className="text-center">
            <div className="mx-auto h-16 w-16 bg-yellow-100 rounded-full flex items-center justify-center mb-4">
              <span className="text-yellow-600 text-2xl">?</span>
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-1">Task Not Found</h3>
            <p className="text-gray-500 mb-4">The requested task could not be found.</p>
            <Button 
              variant="primary" 
              size="md"
              onClick={() => router.back()}
            >
              Go Back
            </Button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-2xl mx-auto px-4 py-8">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold text-gray-800">Task Details</h1>
          <Button 
            variant="secondary" 
            size="md"
            onClick={() => router.back()}
          >
            Back to Tasks
          </Button>
        </div>

        {isEditing ? (
          <TaskForm
            task={task}
            onSubmit={handleUpdateTask}
            onCancel={handleCancelEdit}
          />
        ) : (
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex justify-between items-start mb-4">
              <h2 className={`text-2xl font-bold ${task.completed ? 'line-through text-gray-500' : 'text-gray-800'}`}>
                {task.title}
              </h2>
              <div className="flex space-x-2">
                <Button 
                  variant={task.completed ? "secondary" : "primary"} 
                  size="sm"
                  onClick={handleToggleComplete}
                >
                  {task.completed ? 'Undo' : 'Complete'}
                </Button>
                <Button 
                  variant="secondary" 
                  size="sm"
                  onClick={() => setIsEditing(true)}
                >
                  Edit
                </Button>
              </div>
            </div>

            {task.description && (
              <div className="mb-6">
                <h3 className="text-sm font-medium text-gray-700 mb-2">Description</h3>
                <p className="text-gray-600 bg-gray-50 p-3 rounded-md">
                  {task.description}
                </p>
              </div>
            )}

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-gray-600">
              <div>
                <h3 className="text-xs font-medium text-gray-500 uppercase tracking-wide">Status</h3>
                <p className={task.completed ? 'text-green-600 font-medium' : 'text-yellow-600 font-medium'}>
                  {task.completed ? 'Completed' : 'Pending'}
                </p>
              </div>
              <div>
                <h3 className="text-xs font-medium text-gray-500 uppercase tracking-wide">Created</h3>
                <p>{new Date(task.created_at).toLocaleString()}</p>
              </div>
              <div>
                <h3 className="text-xs font-medium text-gray-500 uppercase tracking-wide">Updated</h3>
                <p>{new Date(task.updated_at).toLocaleString()}</p>
              </div>
              <div>
                <h3 className="text-xs font-medium text-gray-500 uppercase tracking-wide">ID</h3>
                <p className="font-mono text-xs">{task.id.substring(0, 8)}...</p>
              </div>
            </div>

            <div className="mt-8 pt-6 border-t border-gray-200">
              <Button 
                variant="danger" 
                size="md"
                onClick={handleDeleteTask}
              >
                Delete Task
              </Button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default TaskDetailPage;