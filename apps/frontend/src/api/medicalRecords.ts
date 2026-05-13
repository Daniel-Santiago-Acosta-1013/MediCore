import { client } from './client'
import type { MedicalRecord, ListParams } from '@/types'

export const medicalRecordsApi = {
  list: (params?: ListParams) => client.get<MedicalRecord[]>('/medical-records', params),
  get: (id: string) => client.get<MedicalRecord>(`/medical-records/${id}`),
  create: (data: Omit<MedicalRecord, 'id' | 'created_at'>) => client.post<MedicalRecord>('/medical-records', data),
  update: (id: string, data: Partial<MedicalRecord>) => client.put<MedicalRecord>(`/medical-records/${id}`, data),
  remove: (id: string) => client.delete<void>(`/medical-records/${id}`),
}
