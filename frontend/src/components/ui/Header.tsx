import { Sparkles, LogOut } from 'lucide-react';
import { useAuth } from '../../hooks/useAuth';

export default function Header() {
  const { logout } = useAuth();

  return (
    <header className="bg-white/90 backdrop-blur-sm shadow-sm sticky top-0 z-10">
      <div className="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8 flex justify-between items-center">
        <div className="flex items-center">
          <Sparkles className="h-6 w-6 text-primary" />
          <h1 className="text-xl font-bold text-gray-900 ml-2">Resume AI</h1>
        </div>
        <button onClick={logout} className="flex items-center text-sm font-medium text-gray-500 hover:text-primary transition-colors">
          <LogOut size={16} className="mr-1" /> Logout
        </button>
      </div>
    </header>
  );
}