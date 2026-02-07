import React from 'react';
import { TrashIcon, PencilIcon } from '@heroicons/react/24/outline';

interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

interface TaskCardProps {
  task: Task;
  onEdit: (task: Task) => void;
  onDelete: (taskId: string) => void;
  onToggleComplete: (taskId: string) => void;
}

const TaskCard: React.FC<TaskCardProps> = ({ task, onEdit, onDelete, onToggleComplete }) => {
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className={`bg-white rounded-lg shadow-md p-4 mb-3 border-l-4 ${
      task.completed ? 'border-green-500' : 'border-blue-500'
    } transition-all duration-200 hover:shadow-lg`}>
      <div className="flex justify-between items-start">
        <div className="flex items-center">
          <input
            type="checkbox"
            checked={task.completed}
            onChange={() => onToggleComplete(task.id)}
            className="h-5 w-5 text-blue-600 rounded focus:ring-blue-500 border-gray-300 mr-3"
          />
          <div>
            <h3 className={`text-lg font-medium ${
              task.completed ? 'line-through text-gray-500' : 'text-gray-800'
            }`}>
              {task.title}
            </h3>
            {task.description && (
              <p className={`mt-1 text-sm ${
                task.completed ? 'text-gray-400' : 'text-gray-600'
              }`}>
                {task.description}
              </p>
            )}
          </div>
        </div>
        <div className="flex space-x-2">
          <button
            onClick={() => onEdit(task)}
            className="text-blue-600 hover:text-blue-800 transition-colors"
            aria-label="Edit task"
          >
            <PencilIcon className="h-5 w-5" />
          </button>
          <button
            onClick={() => onDelete(task.id)}
            className="text-red-600 hover:text-red-800 transition-colors"
            aria-label="Delete task"
          >
            <TrashIcon className="h-5 w-5" />
          </button>
        </div>
      </div>
      <div className="mt-2 text-xs text-gray-500">
        Created: {formatDate(task.created_at)}
        {task.updated_at !== task.created_at && (
          <span>, Updated: {formatDate(task.updated_at)}</span>
        )}
      </div>
    </div>
  );
};

export default TaskCard;