import React, { createContext, useContext, useState, useCallback, useEffect } from 'react'
import { authApi } from '@/api/auth'
import { client } from '@/api/client'
import type { User, Token } from '@/types'

interface AuthContextType {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  login: (username: string, password: string) => Promise<void>
  register: (email: string, full_name: string, password: string, role?: User['role']) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextType | null>(null)

const TOKEN_KEY = 'medicore_token'

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  const initAuth = useCallback(async () => {
    const token = localStorage.getItem(TOKEN_KEY)
    if (token) {
      client.setToken(token)
      try {
        const me = await authApi.me()
        setUser(me)
      } catch {
        localStorage.removeItem(TOKEN_KEY)
        client.setToken(null)
      }
    }
    setIsLoading(false)
  }, [])

  useEffect(() => {
    initAuth()
  }, [initAuth])

  const login = useCallback(async (username: string, password: string) => {
    const token: Token = await authApi.login({ username, password })
    localStorage.setItem(TOKEN_KEY, token.access_token)
    client.setToken(token.access_token)
    const me = await authApi.me()
    setUser(me)
  }, [])

  const register = useCallback(async (email: string, full_name: string, password: string, role?: User['role']) => {
    await authApi.register({ email, full_name, password, role })
    const token: Token = await authApi.login({ username: email, password })
    localStorage.setItem(TOKEN_KEY, token.access_token)
    client.setToken(token.access_token)
    const me = await authApi.me()
    setUser(me)
  }, [])

  const logout = useCallback(() => {
    localStorage.removeItem(TOKEN_KEY)
    client.setToken(null)
    setUser(null)
  }, [])

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: !!user,
        isLoading,
        login,
        register,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) throw new Error('useAuth must be used within AuthProvider')
  return context
}
