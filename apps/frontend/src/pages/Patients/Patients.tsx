import React, { useState, useEffect, useCallback } from 'react'
import { patientsApi } from '@/api/patients'
import { Button } from '@/components/Button/Button'
import { Input } from '@/components/Input/Input'
import { Table } from '@/components/Table/Table'
import { Modal } from '@/components/Modal/Modal'
import { Loading } from '@/components/Loading/Loading'
import { EmptyState } from '@/components/EmptyState/EmptyState'
import type { Patient } from '@/types'
import { useToast } from '@/stores/ToastContext'
import '../Users/Users.css'

export function Patients() {
  const { showToast } = useToast()
  const [patients, setPatients] = useState<Patient[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [editingPatient, setEditingPatient] = useState<Patient | null>(null)
  const [formData, setFormData] = useState<Partial<Patient>>({})
  const [isSubmitting, setIsSubmitting] = useState(false)

  const fetchPatients = useCallback(async () => {
    setIsLoading(true)
    try {
      const data = await patientsApi.list()
      setPatients(data)
    } catch (err: any) {
      showToast(err.message || 'Error al cargar pacientes', 'error')
    } finally {
      setIsLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchPatients()
  }, [fetchPatients])

  const openCreate = () => {
    setEditingPatient(null)
    setFormData({})
    setIsModalOpen(true)
  }

  const openEdit = (patient: Patient) => {
    setEditingPatient(patient)
    setFormData({ ...patient })
    setIsModalOpen(true)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)
    try {
      if (editingPatient) {
        await patientsApi.update(editingPatient.id, formData)
        showToast('Paciente actualizado correctamente', 'success')
      } else {
        await patientsApi.create(formData as Omit<Patient, 'id' | 'created_at'>)
        showToast('Paciente creado correctamente', 'success')
      }
      setIsModalOpen(false)
      fetchPatients()
    } catch (err: any) {
      showToast(err.message || 'Error al guardar paciente', 'error')
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleDelete = async (id: string) => {
    if (!confirm('¿Eliminar este paciente?')) return
    try {
      await patientsApi.remove(id)
      showToast('Paciente eliminado correctamente', 'success')
      fetchPatients()
    } catch (err: any) {
      showToast(err.message || 'Error al eliminar paciente', 'error')
    }
  }

  const columns = [
    { key: 'date_of_birth', header: 'Nacimiento', render: (p: Patient) => p.date_of_birth || '-' },
    { key: 'phone', header: 'Teléfono', render: (p: Patient) => p.phone || '-' },
    { key: 'address', header: 'Dirección', render: (p: Patient) => p.address || '-' },
    {
      key: 'actions',
      header: '',
      width: '100px',
      render: (p: Patient) => (
        <div className="actions-cell">
          <button className="btn-action" onClick={() => openEdit(p)} title="Editar">
            <svg width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L10.582 16.07a4.5 4.5 0 01-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 011.13-1.897l8.932-8.931zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0115.75 21H5.25A2.25 2.25 0 013 18.75V8.25A2.25 2.25 0 015.25 6H10" />
            </svg>
          </button>
          <button className="btn-action delete" onClick={() => handleDelete(p.id)} title="Eliminar">
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
          <h1 className="page-title">Pacientes</h1>
          <p className="page-subtitle">Gestiona los pacientes del hospital</p>
        </div>
        <Button onClick={openCreate}>Nuevo paciente</Button>
      </div>

      {isLoading ? (
        <Loading />
      ) : patients.length === 0 ? (
        <EmptyState
          title="No hay pacientes"
          description="Comienza creando el primer paciente."
          actionLabel="Crear paciente"
          onAction={openCreate}
        />
      ) : (
        <Table columns={columns} data={patients} keyExtractor={(p) => p.id} />
      )}

      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title={editingPatient ? 'Editar paciente' : 'Nuevo paciente'}
        footer={
          <>
            <Button variant="secondary" onClick={() => setIsModalOpen(false)}>
              Cancelar
            </Button>
            <Button onClick={handleSubmit} isLoading={isSubmitting}>
              {editingPatient ? 'Guardar cambios' : 'Crear paciente'}
            </Button>
          </>
        }
      >
        <form className="crud-form" onSubmit={handleSubmit}>
          <div className="crud-form-row">
            <Input
              label="Fecha de nacimiento"
              type="date"
              value={formData.date_of_birth || ''}
              onChange={(e) => setFormData({ ...formData, date_of_birth: e.target.value })}
            />
            <Input
              label="Teléfono"
              value={formData.phone || ''}
              onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
            />
          </div>
          <Input
            label="Dirección"
            value={formData.address || ''}
            onChange={(e) => setFormData({ ...formData, address: e.target.value })}
          />
          <div className="crud-form-row">
            <Input
              label="Contacto de emergencia"
              value={formData.emergency_contact_name || ''}
              onChange={(e) => setFormData({ ...formData, emergency_contact_name: e.target.value })}
            />
            <Input
              label="Teléfono de emergencia"
              value={formData.emergency_contact_phone || ''}
              onChange={(e) => setFormData({ ...formData, emergency_contact_phone: e.target.value })}
            />
          </div>
        </form>
      </Modal>
    </div>
  )
}
