import { client } from './client'
import type { UserRegister, Token, LoginCredentials, User } from '@/types'

export const authApi = {
  login: (data: LoginCredentials) => {
    const body = new URLSearchParams()
    body.append('username', data.username)
    body.append('password', data.password)
    return client.request<Token>('/auth/login', {
      method: 'POST',
      body: body.toString(),
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    })
  },

  register: (data: UserRegister) =>
    client.post<User>('/auth/register', data),

  me: () => client.get<User>('/auth/me'),
}
