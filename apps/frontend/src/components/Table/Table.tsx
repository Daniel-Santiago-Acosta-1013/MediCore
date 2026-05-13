import React from 'react'
import './Table.css'

interface Column<T> {
  key: string
  header: string
  render?: (item: T) => React.ReactNode
  width?: string
}

interface TableProps<T> {
  columns: Column<T>[]
  data: T[]
  keyExtractor: (item: T) => string
  isLoading?: boolean
  emptyMessage?: string
}

export function Table<T>({ columns, data, keyExtractor, isLoading, emptyMessage = 'No hay datos' }: TableProps<T>) {
  if (isLoading) {
    return (
      <div className="table-container">
        <div className="table-empty">Cargando...</div>
      </div>
    )
  }

  if (data.length === 0) {
    return (
      <div className="table-container">
        <div className="table-empty">{emptyMessage}</div>
      </div>
    )
  }

  return (
    <div className="table-container">
      <table className="table">
        <thead>
          <tr>
            {columns.map((col) => (
              <th key={col.key} style={col.width ? { width: col.width } : undefined}>
                {col.header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((item) => (
            <tr key={keyExtractor(item)}>
              {columns.map((col) => (
                <td key={col.key}>
                  {col.render ? col.render(item) : (item as Record<string, unknown>)[col.key] as React.ReactNode}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
