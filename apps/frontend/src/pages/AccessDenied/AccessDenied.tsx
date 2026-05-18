import { useNavigate } from 'react-router-dom'
import { Button } from '@/components/Button/Button'
import './AccessDenied.css'

export function AccessDenied() {
  const navigate = useNavigate()

  return (
    <div className="access-denied">
      <div className="access-denied-icon">
        <svg width="64" height="64" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
          <path strokeLinecap="round" strokeLinejoin="round" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636" />
        </svg>
      </div>
      <h2 className="access-denied-title">Acceso restringido</h2>
      <p className="access-denied-description">
        No tienes permisos para ver esta sección. Contacta al administrador si crees que esto es un error.
      </p>
      <Button onClick={() => navigate(-1)}>Volver atrás</Button>
    </div>
  )
}
