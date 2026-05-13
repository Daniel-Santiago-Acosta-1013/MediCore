import React from 'react'
import './Card.css'

interface CardProps {
  title?: string
  subtitle?: string
  action?: React.ReactNode
  children: React.ReactNode
}

export function Card({ title, subtitle, action, children }: CardProps) {
  return (
    <div className="card">
      {(title || action) && (
        <div className="card-header">
          <div>
            {title && <h3 className="card-title">{title}</h3>}
            {subtitle && <p className="card-subtitle">{subtitle}</p>}
          </div>
          {action}
        </div>
      )}
      {children}
    </div>
  )
}
