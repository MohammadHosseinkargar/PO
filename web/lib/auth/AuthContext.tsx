import { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { User, getUserFromToken, refreshToken } from './auth';

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  register: (email: string, password: string, name: string) => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const initAuth = async () => {
      const token = localStorage.getItem('token');
      if (token) {
        const user = getUserFromToken(token);
        if (!user) {
          const newToken = await refreshToken();
          if (newToken) {
            setUser(getUserFromToken(newToken));
          }
        } else {
          setUser(user);
        }
      }
      setLoading(false);
    };

    initAuth();
  }, []);

  const value = {
    user,
    loading,
    login: async (email: string, password: string) => {
      const user = await login(email, password);
      setUser(user);
    },
    logout: async () => {
      await logout();
      setUser(null);
    },
    register: async (email: string, password: string, name: string) => {
      await register(email, password, name);
    },
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}