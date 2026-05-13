import { client } from './client'
import type { User, UserCreate, ListParams } from '@/types'

export const usersApi = {
  list: (params?: ListParams) => client.get<User[]>('/users', params),
  get: (id: string) => client.get<User>(`/users/${id}`),
  create: (data: UserCreate) => client.post<User>('/users', data),
  update: (id: string, data: Partial<UserCreate>) => client.put<User>(`/users/${id}`, data),
  remove: (id: string) => client.delete<void>(`/users/${id}`),
}
