import { useForm } from 'react-hook-form';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import toast from 'react-hot-toast';

export default function SignupPage() {
  const { register, handleSubmit } = useForm();
  const { signup } = useAuth();
  const navigate = useNavigate();

  const onSubmit = async (data: any) => {
    try {
      await toast.promise(signup(data), {
        loading: 'Creating account...',
        success: 'Account created! Please log in.',
        error: 'Failed to create account.',
      });
      navigate('/login');
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-50">
      <div className="p-8 bg-white rounded-xl shadow-lg w-full max-w-md">
        <h2 className="text-3xl font-bold mb-6 text-center text-gray-800">Create an Account</h2>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div>
            <label className="block mb-2 text-sm font-medium text-gray-600">Full Name</label>
            <input {...register('name')} type="text" required className="w-full px-4 py-2 border rounded-lg"/>
          </div>
          <div>
            <label className="block mb-2 text-sm font-medium text-gray-600">Email</label>
            <input {...register('email')} type="email" required className="w-full px-4 py-2 border rounded-lg"/>
          </div>
          <div>
            <label className="block mb-2 text-sm font-medium text-gray-600">Password</label>
            <input {...register('password')} type="password" required className="w-full px-4 py-2 border rounded-lg"/>
          </div>
          <button type="submit" className="w-full py-3 font-bold bg-blue-600 text-white rounded-lg hover:bg-blue-700">
            Sign Up
          </button>
        </form>
        <p className="text-center text-sm text-gray-600 mt-6">
          Already have an account?{' '}
          <Link to="/login" className="font-medium text-blue-600 hover:underline">
            Sign In
          </Link>
        </p>
      </div>
    </div>
  );
}