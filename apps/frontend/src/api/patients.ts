import { client } from './client'
import type { Patient, ListParams } from '@/types'

export const patientsApi = {
  list: (params?: ListParams) => client.get<Patient[]>('/patients', params),
  get: (id: string) => client.get<Patient>(`/patients/${id}`),
  create: (data: Omit<Patient, 'id' | 'created_at'>) => client.post<Patient>('/patients', data),
  update: (id: string, data: Partial<Patient>) => client.put<Patient>(`/patients/${id}`, data),
  remove: (id: string) => client.delete<void>(`/patients/${id}`),
}
