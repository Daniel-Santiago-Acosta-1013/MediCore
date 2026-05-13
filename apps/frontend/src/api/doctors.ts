import { client } from './client'
import type { Doctor, ListParams } from '@/types'

export const doctorsApi = {
  list: (params?: ListParams) => client.get<Doctor[]>('/doctors', params),
  get: (id: string) => client.get<Doctor>(`/doctors/${id}`),
  create: (data: Omit<Doctor, 'id' | 'created_at'>) => client.post<Doctor>('/doctors', data),
  update: (id: string, data: Partial<Doctor>) => client.put<Doctor>(`/doctors/${id}`, data),
  remove: (id: string) => client.delete<void>(`/doctors/${id}`),
}
