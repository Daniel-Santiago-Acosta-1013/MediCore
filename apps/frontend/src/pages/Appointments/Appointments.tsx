import React, { useState, useEffect, useCallback } from 'react'
import { appointmentsApi } from '@/api/appointments'
import { doctorsApi } from '@/api/doctors'
import { Button } from '@/components/Button/Button'
import { Input } from '@/components/Input/Input'
import { Table } from '@/components/Table/Table'
import { Modal } from '@/components/Modal/Modal'
import { Loading } from '@/components/Loading/Loading'
import { EmptyState } from '@/components/EmptyState/EmptyState'
import { useAuth } from '@/stores/AuthContext'
import type { Appointment, Doctor } from '@/types'
import '../Users/Users.css'

const statuses: Appointment['status'][] = ['SCHEDULED', 'COMPLETED', 'CANCELLED']

export function Appointments() {
  const { user } = useAuth()
  const [appointments, setAppointments] = useState<Appointment[]>([])
  const [doctors, setDoctors] = useState<Doctor[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [editingAppointment, setEditingAppointment] = useState<Appointment | null>(null)
  const [formData, setFormData] = useState<Partial<Appointment>>({})
  const [isSubmitting, setIsSubmitting] = useState(false)

  const isPatient = user?.role === 'PATIENT'

  const fetchAppointments = useCallback(async () => {
    setIsLoading(true)
    try {
      const data = await appointmentsApi.list()
      setAppointments(data)
    } catch {
      // silent
    } finally {
      setIsLoading(false)
    }
  }, [])

  const fetchDoctors = useCallback(async () => {
    try {
      const data = await doctorsApi.list()
      setDoctors(data)
    } catch {
      // silent
    }
  }, [])

  useEffect(() => {
    fetchAppointments()
    fetchDoctors()
  }, [fetchAppointments, fetchDoctors])

  const openCreate = () => {
    setEditingAppointment(null)
    setFormData({
      status: 'SCHEDULED',
      patient_id: isPatient ? user?.id : undefined,
    })
    setIsModalOpen(true)
  }

  const openEdit = (appointment: Appointment) => {
    setEditingAppointment(appointment)
    setFormData({ ...appointment })
    setIsModalOpen(true)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)
    try {
      if (editingAppointment) {
        await appointmentsApi.update(editingAppointment.id, formData)
      } else {
        await appointmentsApi.create(formData as Omit<Appointment, 'id' | 'created_at'>)
      }
      setIsModalOpen(false)
      fetchAppointments()
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleDelete = async (id: string) => {
    if (!confirm('¿Eliminar esta cita?')) return
    await appointmentsApi.remove(id)
    fetchAppointments()
  }

  const statusBadge = (status: Appointment['status']) => {
    const map: Record<string, string> = {
      SCHEDULED: 'badge-primary',
      COMPLETED: 'badge-success',
      CANCELLED: 'badge-danger',
    }
    return <span className={`badge ${map[status]}`}>{status}</span>
  }

  const columns = [
    { key: 'patient_id', header: 'Paciente' },
    { key: 'doctor_id', header: 'Doctor' },
    { key: 'scheduled_at', header: 'Fecha', render: (a: Appointment) => a.scheduled_at || '-' },
    { key: 'status', header: 'Estado', render: (a: Appointment) => statusBadge(a.status) },
    { key: 'notes', header: 'Notas', render: (a: Appointment) => a.notes || '-' },
    {
      key: 'actions',
      header: '',
      width: '100px',
      render: (a: Appointment) => (
        <div className="actions-cell">
          <button className="btn-action" onClick={() => openEdit(a)} title="Editar">
            <svg width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L10.582 16.07a4.5 4.5 0 01-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 011.13-1.897l8.932-8.931zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0115.75 21H5.25A2.25 2.25 0 013 18.75V8.25A2.25 2.25 0 015.25 6H10" />
            </svg>
          </button>
          <button className="btn-action delete" onClick={() => handleDelete(a.id)} title="Eliminar">
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
          <h1 className="page-title">Citas</h1>
          <p className="page-subtitle">Gestiona las citas médicas</p>
        </div>
        <Button onClick={openCreate}>Nueva cita</Button>
      </div>

      {isLoading ? (
        <Loading />
      ) : appointments.length === 0 ? (
        <EmptyState
          title="No hay citas"
          description="Comienza creando la primera cita médica."
          actionLabel="Nueva cita"
          onAction={openCreate}
        />
      ) : (
        <Table columns={columns} data={appointments} keyExtractor={(a) => a.id} />
      )}

      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title={editingAppointment ? 'Editar cita' : 'Nueva cita'}
        footer={
          <>
            <Button variant="secondary" onClick={() => setIsModalOpen(false)}>
              Cancelar
            </Button>
            <Button onClick={handleSubmit} isLoading={isSubmitting}>
              {editingAppointment ? 'Guardar cambios' : 'Crear cita'}
            </Button>
          </>
        }
      >
        <form className="crud-form" onSubmit={handleSubmit}>
          <div className="crud-form-row">
            {!isPatient && (
              <Input
                label="Paciente ID"
                value={formData.patient_id || ''}
                onChange={(e) => setFormData({ ...formData, patient_id: e.target.value })}
                required
              />
            )}
            <div className="input-group" style={{ flex: 1 }}>
              <label className="input-label">Doctor</label>
              <select
                className="input"
                value={formData.doctor_id || ''}
                onChange={(e) => setFormData({ ...formData, doctor_id: e.target.value })}
                required
              >
                <option value="">Selecciona un doctor</option>
                {doctors.map((doctor) => (
                  <option key={doctor.id} value={doctor.id}>
                    {doctor.full_name} — {doctor.specialty} ({doctor.license_number})
                  </option>
                ))}
              </select>
            </div>
          </div>
          <Input
            label="Fecha y hora"
            type="datetime-local"
            value={formData.scheduled_at || ''}
            onChange={(e) => setFormData({ ...formData, scheduled_at: e.target.value })}
            required
          />
          <div className="input-group">
            <label className="input-label">Estado</label>
            <select
              className="input"
              value={formData.status || 'SCHEDULED'}
              onChange={(e) => setFormData({ ...formData, status: e.target.value as Appointment['status'] })}
            >
              {statuses.map((s) => (
                <option key={s} value={s}>
                  {s}
                </option>
              ))}
            </select>
          </div>
          <Input
            label="Notas"
            value={formData.notes || ''}
            onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
          />
        </form>
      </Modal>
    </div>
  )
}
