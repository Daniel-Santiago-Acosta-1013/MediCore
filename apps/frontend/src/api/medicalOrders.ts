import { client } from './client'
import type { MedicalOrder, ListParams } from '@/types'

export const medicalOrdersApi = {
  list: (params?: ListParams) => client.get<MedicalOrder[]>('/medical-orders', params),
  get: (id: string) => client.get<MedicalOrder>(`/medical-orders/${id}`),
  create: (data: Omit<MedicalOrder, 'id' | 'created_at'>) => client.post<MedicalOrder>('/medical-orders', data),
  update: (id: string, data: Partial<MedicalOrder>) => client.put<MedicalOrder>(`/medical-orders/${id}`, data),
  remove: (id: string) => client.delete<void>(`/medical-orders/${id}`),
}
