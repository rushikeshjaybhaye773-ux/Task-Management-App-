import axios from 'axios';
import { Task, User } from '@/types/task';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_URL,
});

export const authenticateGoogle = async (token: string) => {
  const response = await api.post('/auth/google', { token });
  return response.data;
};

export const fetchUsers = async (): Promise<User[]> => {
  const response = await api.get('/users');
  return response.data;
};

export const fetchTasks = async (userId: string): Promise<Task[]> => {
  const response = await api.get(`/tasks?user_id=${userId}`);
  return response.data;
};

export const createTask = async (data: { title: string; description: string; created_by: string; assigned_to?: string }) => {
  const response = await api.post('/tasks', data);
  return response.data;
};

export const completeTask = async (taskId: string) => {
  const response = await api.put(`/tasks/${taskId}/complete`);
  return response.data;
};
