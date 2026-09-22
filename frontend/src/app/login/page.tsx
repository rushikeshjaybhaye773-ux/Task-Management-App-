'use client';
import { GoogleLogin } from '@react-oauth/google';
import { authenticateGoogle } from '@/lib/api';
import { useRouter } from 'next/navigation';

export default function LoginPage() {
  const router = useRouter();

  const handleSuccess = async (credentialResponse: any) => {
    try {
      const { credential } = credentialResponse;
      const res = await authenticateGoogle(credential);
      
      if (res.user) {
        // Simple client-side auth for the assignment
        localStorage.setItem('user', JSON.stringify(res.user));
        router.push('/dashboard');
      }
    } catch (error) {
      console.error('Login failed', error);
      alert('Login failed. Please try again.');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="max-w-md w-full p-8 bg-white rounded-lg shadow-md flex flex-col items-center">
        <h2 className="text-2xl font-bold mb-6 text-center text-gray-800">Task Management</h2>
        <p className="text-gray-600 mb-8 text-center">Login to manage your tasks efficiently</p>
        
        <div className="w-full flex justify-center">
          <GoogleLogin
            onSuccess={handleSuccess}
            onError={() => {
              console.log('Login Failed');
            }}
          />
        </div>
      </div>
    </div>
  );
}
