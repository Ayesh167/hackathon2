// API client library for frontend-backend communication
import { Task, CreateTaskData, UpdateTaskData } from './types/task';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface ApiResponse<T> {
  data?: T;
  error?: string;
}

// Real authentication functions
const auth = {
  login: async (email: string, password: string) => {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });

    if (response.ok) {
      const data = await response.json();
      localStorage.setItem('jwt_token', data.access_token);
      return { data };
    } else {
      const errorData = await response.json().catch(() => ({ detail: 'Login failed' }));
      throw new Error(errorData.detail || 'Login failed');
    }
  },

  signup: async (email: string, password: string, name: string) => {
    const response = await fetch(`${API_BASE_URL}/auth/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password, name }),
    });

    if (response.ok) {
      const data = await response.json();
      localStorage.setItem('jwt_token', data.access_token);
      return { data };
    } else {
      const errorData = await response.json().catch(() => ({ detail: 'Signup failed' }));
      throw new Error(errorData.detail || 'Signup failed');
    }
  }
};

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  // Helper method to get JWT token from localStorage
  private getToken(): string | null {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('jwt_token');
    }
    return null;
  }

  // Helper method to create headers with JWT token
  private getHeaders(): HeadersInit {
    const token = this.getToken();
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    };

    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    return headers;
  }

  // Generic request method
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    try {
      const url = `${this.baseUrl}${endpoint}`;
      const response = await fetch(url, {
        ...options,
        headers: { ...this.getHeaders(), ...options.headers },
      });

      if (!response.ok) {
        const errorData = await response.text();
        throw new Error(errorData || `HTTP error! status: ${response.status}`);
      }

      if (response.status === 204) {
        // No content for DELETE requests
        return { data: undefined as unknown as T };
      }

      const data = await response.json();
      return { data };
    } catch (error: any) {
      console.error('API request failed:', error);
      return { error: error.message || 'Unknown error occurred' };
    }
  }

  // User authentication methods (will try real endpoints first, then mock)
  async login(email: string, password: string): Promise<ApiResponse<{ access_token: string; token_type: string; user: any }>> {
    return auth.login(email, password);
  }

  async signup(email: string, password: string, name: string): Promise<ApiResponse<{ access_token: string; token_type: string; user: any }>> {
    return auth.signup(email, password, name);
  }

  async logout(): Promise<void> {
    localStorage.removeItem('jwt_token');
  }

  // User API methods
  async getUserDetails(): Promise<ApiResponse<any>> {
    return this.request('/auth/me');
  }

  async updateUser(userData: { name: string; email: string }): Promise<ApiResponse<any>> {
    return this.request('/auth/me', {
      method: 'PUT',
      body: JSON.stringify(userData),
    });
  }

  async changePassword(passwordData: { current_password: string; new_password: string }): Promise<ApiResponse<any>> {
    return this.request('/auth/change-password', {
      method: 'POST',
      body: JSON.stringify(passwordData),
    });
  }

  async getActiveSessions(): Promise<ApiResponse<any>> {
    return this.request('/auth/active-sessions');
  }

  async revokeSession(sessionId: string): Promise<ApiResponse<any>> {
    return this.request(`/auth/active-sessions/${sessionId}`, {
      method: 'DELETE',
    });
  }

  async getTwoFactorStatus(): Promise<ApiResponse<any>> {
    return this.request('/auth/two-factor');
  }

  async setupTwoFactor(): Promise<ApiResponse<any>> {
    return this.request('/auth/two-factor/setup', {
      method: 'POST',
    });
  }

  async verifyTwoFactor(token: string): Promise<ApiResponse<any>> {
    return this.request('/auth/two-factor/verify', {
      method: 'POST',
      body: JSON.stringify({ token }),
    });
  }

  async disableTwoFactor(): Promise<ApiResponse<any>> {
    return this.request('/auth/two-factor/disable', {
      method: 'POST',
    });
  }

  // Task API methods
  async getTasks(userId: string): Promise<ApiResponse<Task[]>> {
    return this.request(`/api/${userId}/tasks`);
  }

  async createTask(userId: string, taskData: CreateTaskData): Promise<ApiResponse<Task>> {
    return this.request(`/api/${userId}/tasks`, {
      method: 'POST',
      body: JSON.stringify(taskData),
    });
  }

  async getTask(userId: string, taskId: string): Promise<ApiResponse<Task>> {
    return this.request(`/api/${userId}/tasks/${taskId}`);
  }

  async updateTask(
    userId: string,
    taskId: string,
    taskData: UpdateTaskData
  ): Promise<ApiResponse<Task>> {
    return this.request(`/api/${userId}/tasks/${taskId}`, {
      method: 'PUT',
      body: JSON.stringify(taskData),
    });
  }

  async deleteTask(userId: string, taskId: string): Promise<ApiResponse<void>> {
    return this.request(`/api/${userId}/tasks/${taskId}`, {
      method: 'DELETE',
    });
  }

  async toggleTaskCompletion(userId: string, taskId: string): Promise<ApiResponse<Task>> {
    return this.request(`/api/${userId}/tasks/${taskId}/complete`, {
      method: 'PATCH',
    });
  }

  // Chat API methods
  async sendMessage(message: string, conversationId?: string): Promise<ApiResponse<any>> {
    return this.request('/api/chat', {
      method: 'POST',
      body: JSON.stringify({
        message,
        conversation_id: conversationId
      }),
    });
  }

  async getConversations(): Promise<ApiResponse<any[]>> {
    return this.request('/api/conversations');
  }

  async getConversation(conversationId: string): Promise<ApiResponse<any>> {
    return this.request(`/api/conversations/${conversationId}`);
  }
}

export const apiClient = new ApiClient(API_BASE_URL);

// Export the ApiClient class for potential extension
export default ApiClient;