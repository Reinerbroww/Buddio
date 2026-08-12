"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from "react";
import { useRouter } from "next/navigation";
import api, { getToken, setToken } from "@/services/api";
import type { TokenResponse, User } from "@/lib/types";

interface RegisterPayload {
  email: string;
  password: string;
  full_name?: string;
  grade_level?: string;
}

interface AuthContextValue {
  user: User | null;
  token: string | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<User>;
  register: (payload: RegisterPayload) => Promise<User>;
  logout: () => void;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setTokenState] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  const refreshUser = useCallback(async () => {
    try {
      const me = await api.get<User>("/users/me");
      setUser(me);
    } catch {
      setUser(null);
      setTokenState(null);
      setToken(null);
    }
  }, []);

  useEffect(() => {
    const t = getToken();
    if (t) {
      Promise.resolve(t).then(setTokenState);
      Promise.resolve()
        .then(refreshUser)
        .finally(() => setLoading(false));
      return;
    }
    Promise.resolve().then(() => setLoading(false));
  }, [refreshUser]);

  useEffect(() => {
    const onUnauthorized = () => {
      setUser(null);
      setTokenState(null);
      router.push("/login");
    };
    window.addEventListener("buddio:unauthorized", onUnauthorized);
    return () => window.removeEventListener("buddio:unauthorized", onUnauthorized);
  }, [router]);

  const login = useCallback(async (email: string, password: string) => {
    const res = await api.post<TokenResponse>("/auth/login", { email, password });
    setToken(res.access_token);
    setTokenState(res.access_token);
    const me = await api.get<User>("/users/me");
    setUser(me);
    return me;
  }, []);

  const register = useCallback(async (payload: RegisterPayload) => {
    const user = await api.post<User>("/auth/register", payload);
    const res = await api.post<TokenResponse>("/auth/login", {
      email: payload.email,
      password: payload.password,
    });
    setToken(res.access_token);
    setTokenState(res.access_token);
    setUser(user);
    return user;
  }, []);

  const logout = useCallback(() => {
    setToken(null);
    setTokenState(null);
    setUser(null);
    router.push("/");
  }, [router]);

  return (
    <AuthContext.Provider
      value={{ user, token, loading, login, register, logout, refreshUser }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth harus dipakai di dalam <AuthProvider>.");
  return ctx;
}
