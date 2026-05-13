import './Loading.css'

export function Loading({ message = 'Cargando...' }: { message?: string }) {
  return (
    <div className="loading">
      <div className="spinner" />
      <span>{message}</span>
    </div>
  )
}
