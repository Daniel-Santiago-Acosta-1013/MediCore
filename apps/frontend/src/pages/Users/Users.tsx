import React, { useState, useEffect, useCallback } from 'react'
import { usersApi } from '@/api/users'
import { Button } from '@/components/Button/Button'
import { Input } from '@/components/Input/Input'
import { Table } from '@/components/Table/Table'
import { Modal } from '@/components/Modal/Modal'
import { Loading } from '@/components/Loading/Loading'
import { EmptyState } from '@/components/EmptyState/EmptyState'
import type { User, UserCreate } from '@/types'
import '../Users/Users.css'

const roles: User['role'][] = ['ADMIN', 'DOCTOR', 'NURSE', 'RECEPTIONIST', 'BILLING', 'PATIENT']

export function Users() {
  const [users, setUsers] = useState<User[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [editingUser, setEditingUser] = useState<User | null>(null)
  const [formData, setFormData] = useState<Partial<UserCreate>>({})
  const [isSubmitting, setIsSubmitting] = useState(false)

  const fetchUsers = useCallback(async () => {
    setIsLoading(true)
    try {
      const data = await usersApi.list()
      setUsers(data)
    } catch {
      // silent
    } finally {
      setIsLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchUsers()
  }, [fetchUsers])

  const openCreate = () => {
    setEditingUser(null)
    setFormData({})
    setIsModalOpen(true)
  }

  const openEdit = (user: User) => {
    setEditingUser(user)
    setFormData({ email: user.email, full_name: user.full_name, role: user.role })
    setIsModalOpen(true)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)
    try {
      if (editingUser) {
        await usersApi.update(editingUser.id, formData)
      } else {
        await usersApi.create(formData as UserCreate)
      }
      setIsModalOpen(false)
      fetchUsers()
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleDelete = async (id: string) => {
    if (!confirm('¿Eliminar este usuario?')) return
    await usersApi.remove(id)
    fetchUsers()
  }

  const columns = [
    { key: 'full_name', header: 'Nombre' },
    { key: 'email', header: 'Correo' },
    {
      key: 'role',
      header: 'Rol',
      render: (u: User) => <span className="badge badge-primary">{u.role}</span>,
    },
    {
      key: 'is_active',
      header: 'Estado',
      render: (u: User) => (
        <span className={`badge ${u.is_active ? 'badge-success' : 'badge-danger'}`}>
          {u.is_active ? 'Activo' : 'Inactivo'}
        </span>
      ),
    },
    {
      key: 'actions',
      header: '',
      width: '100px',
      render: (u: User) => (
        <div className="actions-cell">
          <button className="btn-action" onClick={() => openEdit(u)} title="Editar">
            <svg width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L10.582 16.07a4.5 4.5 0 01-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 011.13-1.897l8.932-8.931zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0115.75 21H5.25A2.25 2.25 0 013 18.75V8.25A2.25 2.25 0 015.25 6H10" />
            </svg>
          </button>
          <button className="btn-action delete" onClick={() => handleDelete(u.id)} title="Eliminar">
            <svg width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
            </svg>
          </button>
        </div>
      ),
    },
  ]

  return (
    <div className="crud-page">
      <div className="page-header">
        <div>
          <h1 className="page-title">Usuarios</h1>
          <p className="page-subtitle">Gestiona los usuarios del sistema</p>
        </div>
        <Button onClick={openCreate}>Nuevo usuario</Button>
      </div>

      {isLoading ? (
        <Loading />
      ) : users.length === 0 ? (
        <EmptyState
          title="No hay usuarios"
          description="Comienza creando el primer usuario del sistema."
          actionLabel="Crear usuario"
          onAction={openCreate}
        />
      ) : (
        <Table columns={columns} data={users} keyExtractor={(u) => u.id} />
      )}

      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title={editingUser ? 'Editar usuario' : 'Nuevo usuario'}
        footer={
          <>
            <Button variant="secondary" onClick={() => setIsModalOpen(false)}>
              Cancelar
            </Button>
            <Button onClick={handleSubmit} isLoading={isSubmitting}>
              {editingUser ? 'Guardar cambios' : 'Crear usuario'}
            </Button>
          </>
        }
      >
        <form className="crud-form" onSubmit={handleSubmit}>
          <Input
            label="Nombre completo"
            value={formData.full_name || ''}
            onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
            required
          />
          <Input
            label="Correo electrónico"
            type="email"
            value={formData.email || ''}
            onChange={(e) => setFormData({ ...formData, email: e.target.value })}
            required
          />
          {!editingUser && (
            <Input
              label="Contraseña"
              type="password"
              value={formData.password || ''}
              onChange={(e) => setFormData({ ...formData, password: e.target.value })}
              required
            />
          )}
          <div className="input-group">
            <label className="input-label">Rol</label>
            <select
              className="input"
              value={formData.role || 'PATIENT'}
              onChange={(e) => setFormData({ ...formData, role: e.target.value as User['role'] })}
            >
              {roles.map((r) => (
                <option key={r} value={r}>
                  {r}
                </option>
              ))}
            </select>
          </div>
        </form>
      </Modal>
    </div>
  )
}
