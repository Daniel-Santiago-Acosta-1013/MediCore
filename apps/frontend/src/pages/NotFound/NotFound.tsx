import { Link } from 'react-router-dom'
import { Button } from '@/components/Button/Button'
import './NotFound.css'

export function NotFound() {
  return (
    <div className="not-found">
      <div className="not-found-code">404</div>
      <h1 className="not-found-title">Página no encontrada</h1>
      <p className="not-found-desc">La página que buscas no existe o fue movida.</p>
      <Link to="/">
        <Button>Volver al inicio</Button>
      </Link>
    </div>
  )
}
