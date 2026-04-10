import { createContext, useState, useEffect } from 'react'
import authService from '../services/authService'

export const AuthContext = createContext()

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('token')
    const role = localStorage.getItem('role')
    if (token && role) {
      setUser({ email: 'user@example.com', role }) // In a real app, you'd decode the token
    }
    setLoading(false)
  }, [])

  const login = async (email, password) => {
    const response = await authService.login(email.trim().toLowerCase(), password)
    setUser({ email: email.trim().toLowerCase(), role: response.role })
    return response
  }

  const signup = async (email, password, role) => {
    const response = await authService.signup(email.trim().toLowerCase(), password, role)
    return response
  }

  const logout = () => {
    authService.logout()
    setUser(null)
  }

  const value = {
    user,
    login,
    signup,
    logout,
    loading,
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}