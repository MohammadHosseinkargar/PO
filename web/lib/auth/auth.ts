import { jwtDecode } from 'jwt-decode';

export interface User {
  id: string;
  email: string;
  name: string;
  role: 'admin' | 'staff' | 'viewer';
}

interface JWTPayload {
  sub: string;
  email: string;
  name: string;
  role: string;
  exp: number;
}

export async function login(email: string, password: string) {
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password }),
  });

  if (!response.ok) {
    throw new Error('Login failed');
  }

  const data = await response.json();
  localStorage.setItem('token', data.access_token);
  localStorage.setItem('refreshToken', data.refresh_token);

  return getUserFromToken(data.access_token);
}

export async function logout() {
  const token = localStorage.getItem('token');
  if (token) {
    try {
      await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/logout`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
    } catch (error) {
      console.error('Logout error:', error);
    }
  }
  localStorage.removeItem('token');
  localStorage.removeItem('refreshToken');
}

export function getUserFromToken(token: string): User | null {
  try {
    const decoded = jwtDecode<JWTPayload>(token);
    if (Date.now() >= decoded.exp * 1000) {
      return null;
    }
    return {
      id: decoded.sub,
      email: decoded.email,
      name: decoded.name,
      role: decoded.role as User['role'],
    };
  } catch {
    return null;
  }
}

export async function refreshToken(): Promise<string | null> {
  const refreshToken = localStorage.getItem('refreshToken');
  if (!refreshToken) return null;

  try {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/refresh`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ refresh_token: refreshToken }),
    });

    if (!response.ok) {
      throw new Error('Token refresh failed');
    }

    const data = await response.json();
    localStorage.setItem('token', data.access_token);
    return data.access_token;
  } catch {
    return null;
  }
}

export async function register(email: string, password: string, name: string) {
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/register`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password, name }),
  });

  if (!response.ok) {
    throw new Error('Registration failed');
  }

  const data = await response.json();
  return data;
}