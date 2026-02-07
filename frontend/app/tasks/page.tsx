'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import TaskCard from '@/components/TaskCard';
import TaskForm from '@/components/TaskForm';
import Button from '@/components/Button';
import { apiClient } from '@/lib/api';

interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
  user_id: string;
}

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

const TasksPage = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [filteredTasks, setFilteredTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [filter, setFilter] = useState<'all' | 'pending' | 'completed'>('all');
  const [sortBy, setSortBy] = useState<'date' | 'title'>('date');
  const [userId, setUserId] = useState<string | null>(null);

  const router = useRouter();

  // Get user ID from JWT token
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

  // Fetch tasks
  useEffect(() => {
    const fetchTasks = async () => {
      if (!userId) return;

      try {
        setLoading(true);
        const response = await apiClient.getTasks(userId);
        
        if (response.error) {
          setError(response.error);
        } else if (response.data) {
          setTasks(response.data);
        }
      } catch (err) {
        setError('Failed to load tasks');
        console.error('Error fetching tasks:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchTasks();
  }, [userId]);

  // Apply filters and sorting
  useEffect(() => {
    let result = [...tasks];

    // Apply filter
    if (filter === 'pending') {
      result = result.filter(task => !task.completed);
    } else if (filter === 'completed') {
      result = result.filter(task => task.completed);
    }

    // Apply sorting
    if (sortBy === 'title') {
      result.sort((a, b) => a.title.localeCompare(b.title));
    } else {
      // Sort by date (newest first)
      result.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());
    }

    setFilteredTasks(result);
  }, [tasks, filter, sortBy]);

  const handleCreateTask = async (taskData: { title: string; description?: string }) => {
    if (!userId) return;

    try {
      const response = await apiClient.createTask(userId, taskData);
      
      if (response.error) {
        console.error('Error creating task:', response.error);
      } else if (response.data) {
        setTasks([...tasks, response.data]);
        setShowForm(false);
      }
    } catch (err) {
      console.error('Error creating task:', err);
    }
  };

  const handleUpdateTask = async (taskData: { title?: string; description?: string; completed?: boolean }) => {
    if (!editingTask || !userId) return;

    try {
      const response = await apiClient.updateTask(userId, editingTask.id, taskData);
      
      if (response.error) {
        console.error('Error updating task:', response.error);
      } else if (response.data) {
        setTasks(tasks.map(t => t.id === editingTask.id ? response.data : t));
        setEditingTask(null);
        setShowForm(false);
      }
    } catch (err) {
      console.error('Error updating task:', err);
    }
  };

  const handleDeleteTask = async (taskId: string) => {
    if (!window.confirm('Are you sure you want to delete this task?')) {
      return;
    }

    if (!userId) return;

    try {
      const response = await apiClient.deleteTask(userId, taskId);
      
      if (response.error) {
        console.error('Error deleting task:', response.error);
      } else {
        setTasks(tasks.filter(task => task.id !== taskId));
      }
    } catch (err) {
      console.error('Error deleting task:', err);
    }
  };

  const handleToggleComplete = async (taskId: string) => {
    if (!userId) return;
    
    const task = tasks.find(t => t.id === taskId);
    if (!task) return;

    try {
      const response = await apiClient.toggleTaskCompletion(userId, taskId);
      
      if (response.error) {
        console.error('Error toggling task completion:', response.error);
      } else if (response.data) {
        setTasks(tasks.map(t => t.id === taskId ? response.data : t));
      }
    } catch (err) {
      console.error('Error toggling task completion:', err);
    }
  };

  const handleEditTask = (task: Task) => {
    setEditingTask(task);
    setShowForm(true);
  };

  const handleCancelForm = () => {
    setShowForm(false);
    setEditingTask(null);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading tasks...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8 gap-4">
          <div>
            <h1 className="text-3xl font-bold text-gray-800">My Tasks</h1>
            <p className="text-gray-600">Manage your tasks efficiently</p>
          </div>
          
          <Button 
            variant="primary" 
            size="md"
            onClick={() => {
              setEditingTask(null);
              setShowForm(true);
            }}
          >
            + New Task
          </Button>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-red-50 text-red-700 rounded-md">
            {error}
          </div>
        )}

        {/* Filters and Sorting */}
        <div className="bg-white rounded-lg shadow-sm p-4 mb-6">
          <div className="flex flex-col md:flex-row gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Filter</label>
              <select
                value={filter}
                onChange={(e) => setFilter(e.target.value as 'all' | 'pending' | 'completed')}
                className="w-full md:w-auto px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="all">All Tasks</option>
                <option value="pending">Pending</option>
                <option value="completed">Completed</option>
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Sort By</label>
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value as 'date' | 'title')}
                className="w-full md:w-auto px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="date">Date</option>
                <option value="title">Title</option>
              </select>
            </div>
          </div>
        </div>

        {/* Task Form */}
        {showForm && (
          <TaskForm
            task={editingTask || undefined}
            onSubmit={editingTask ? handleUpdateTask : handleCreateTask}
            onCancel={handleCancelForm}
          />
        )}

        {/* Task List */}
        <div>
          {filteredTasks.length === 0 ? (
            <div className="bg-white rounded-lg shadow-sm p-8 text-center">
              <div className="mx-auto h-16 w-16 bg-blue-100 rounded-full flex items-center justify-center mb-4">
                <span className="text-blue-600 text-2xl">📋</span>
              </div>
              <h3 className="text-lg font-medium text-gray-900 mb-1">No tasks yet</h3>
              <p className="text-gray-500 mb-4">
                {filter === 'completed' 
                  ? "You haven't completed any tasks yet." 
                  : filter === 'pending' 
                    ? "All tasks are completed!" 
                    : "Get started by creating a new task."}
              </p>
              {filter === 'all' && (
                <Button 
                  variant="primary" 
                  size="md"
                  onClick={() => setShowForm(true)}
                >
                  Create Your First Task
                </Button>
              )}
            </div>
          ) : (
            <div className="space-y-3">
              {filteredTasks.map((task) => (
                <TaskCard
                  key={task.id}
                  task={task}
                  onEdit={handleEditTask}
                  onDelete={handleDeleteTask}
                  onToggleComplete={handleToggleComplete}
                />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default TasksPage;