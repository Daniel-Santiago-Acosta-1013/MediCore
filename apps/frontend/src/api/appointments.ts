import { client } from './client'
import type { Appointment, ListParams } from '@/types'

export const appointmentsApi = {
  list: (params?: ListParams) => client.get<Appointment[]>('/appointments', params),
  get: (id: string) => client.get<Appointment>(`/appointments/${id}`),
  create: (data: Omit<Appointment, 'id' | 'created_at'>) => client.post<Appointment>('/appointments', data),
  update: (id: string, data: Partial<Appointment>) => client.put<Appointment>(`/appointments/${id}`, data),
  remove: (id: string) => client.delete<void>(`/appointments/${id}`),
}
