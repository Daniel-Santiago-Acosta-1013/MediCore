import { client } from './client'
import type { Invoice, ListParams } from '@/types'

export const invoicesApi = {
  list: (params?: ListParams) => client.get<Invoice[]>('/invoices', params),
  get: (id: string) => client.get<Invoice>(`/invoices/${id}`),
  create: (data: Omit<Invoice, 'id' | 'created_at'>) => client.post<Invoice>('/invoices', data),
  update: (id: string, data: Partial<Invoice>) => client.put<Invoice>(`/invoices/${id}`, data),
  remove: (id: string) => client.delete<void>(`/invoices/${id}`),
}
