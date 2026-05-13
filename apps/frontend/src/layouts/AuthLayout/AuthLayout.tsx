import { Outlet } from 'react-router-dom'
import './AuthLayout.css'

export function AuthLayout() {
  return (
    <div className="auth-layout">
      <Outlet />
    </div>
  )
}
