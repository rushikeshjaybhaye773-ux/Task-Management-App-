'use client';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { fetchTasks, completeTask } from '@/lib/api';
import { Task, User } from '@/types/task';

export default function DashboardPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [user, setUser] = useState<User | null>(null);
  const router = useRouter();

  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      const parsedUser = JSON.parse(storedUser);
      setUser(parsedUser);
      loadTasks(parsedUser.id);
    } else {
      router.push('/login');
    }
  }, [router]);

  const loadTasks = async (userId: string) => {
    try {
      const data = await fetchTasks(userId);
      setTasks(data);
    } catch (error) {
      console.error('Failed to fetch tasks', error);
    }
  };

  const handleComplete = async (taskId: string) => {
    try {
      await completeTask(taskId);
      if (user) {
        loadTasks(user.id);
      }
    } catch (error) {
      console.error('Failed to complete task', error);
      alert('Failed to complete task');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('user');
    router.push('/login');
  };

  if (!user) return <div className="p-8">Loading...</div>;

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-800">Welcome, {user.name}</h1>
          <p className="text-gray-500">{user.email}</p>
        </div>
        <div className="flex gap-4">
          <Link href="/tasks/create" className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition">
            + Create Task
          </Link>
          <button onClick={handleLogout} className="px-4 py-2 border border-gray-300 rounded hover:bg-gray-100 transition">
            Logout
          </button>
        </div>
      </div>

      <h2 className="text-xl font-semibold mb-4 text-gray-700">My Tasks</h2>
      
      <div className="space-y-4">
        {tasks.length === 0 ? (
          <p className="text-gray-500">No tasks found.</p>
        ) : (
          tasks.map(task => (
            <div key={task.id} className="p-4 border rounded-lg bg-white shadow-sm flex justify-between items-center">
              <div>
                <h3 className="text-lg font-medium text-gray-800">{task.title}</h3>
                <p className="text-gray-600 text-sm mt-1">{task.description}</p>
                <div className="flex gap-4 mt-3 text-xs text-gray-500">
                  <span>Assigned by: {task.created_by.name}</span>
                  <span>Assigned to: {task.assigned_to ? task.assigned_to.name : 'Unassigned'}</span>
                  <span className={`font-semibold ${task.status === 'COMPLETED' ? 'text-green-600' : 'text-orange-500'}`}>
                    Status: {task.status}
                  </span>
                </div>
              </div>
              
              {task.status !== 'COMPLETED' && task.assigned_to?.id === user.id && (
                <button 
                  onClick={() => handleComplete(task.id)}
                  className="px-4 py-2 bg-green-500 text-white text-sm rounded hover:bg-green-600 transition"
                >
                  Complete
                </button>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
}
