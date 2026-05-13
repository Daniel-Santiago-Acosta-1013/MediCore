import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '@/stores/AuthContext'
import { parseApiError } from '@/utils/errors'
import { Input } from '@/components/Input/Input'
import { Button } from '@/components/Button/Button'
import './Login.css'

export function Login() {
  const { login } = useAuth()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setIsLoading(true)
    try {
      await login(email, password)
    } catch (err) {
      setError(parseApiError(err))
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="auth-card">
      <div className="auth-header">
        <div className="auth-logo">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M12 4v16m8-8H4" />
          </svg>
        </div>
        <h1 className="auth-title">Bienvenido a MediCore</h1>
        <p className="auth-subtitle">Ingresa tus credenciales para continuar</p>
      </div>

      {error && <div className="auth-error">{error}</div>}

      <form className="auth-form" onSubmit={handleSubmit}>
        <Input
          label="Correo electrónico"
          type="email"
          placeholder="tu@email.com"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <Input
          label="Contraseña"
          type="password"
          placeholder="••••••••"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <Button type="submit" isLoading={isLoading}>
          Iniciar sesión
        </Button>
      </form>

      <div className="auth-footer">
        ¿No tienes cuenta? <Link to="/register">Regístrate</Link>
      </div>
    </div>
  )
}
