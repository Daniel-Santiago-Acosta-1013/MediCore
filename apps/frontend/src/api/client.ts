import { reportFrontendApi, reportFrontendError } from './telemetry'

const API_BASE = import.meta.env.VITE_API_URL || '/api'

class ApiClient {
  private token: string | null = null

  setToken(token: string | null) {
    this.token = token
  }

  async request<T>(path: string, options: RequestInit = {}): Promise<T> {
    const url = `${API_BASE}${path}`
    const method = options.method || 'GET'
    const start = performance.now()
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...((options.headers as Record<string, string>) || {}),
    }

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`
    }

    let response: Response
    try {
      response = await fetch(url, {
        ...options,
        headers,
      })
    } catch (error) {
      reportFrontendApi(method, 0, performance.now() - start)
      reportFrontendError('network', error instanceof Error ? error.name : 'NetworkError')
      throw error
    }

    reportFrontendApi(method, response.status, performance.now() - start)

    if (!response.ok) {
      reportFrontendError('api', `HTTP_${response.status}`)
      const error = await response.json().catch(() => ({ detail: 'Error desconocido' }))
      const message = typeof error.detail === 'string'
        ? error.detail
        : JSON.stringify(error.detail)
      throw new Error(message)
    }

    if (response.status === 204) {
      return undefined as T
    }

    return response.json() as Promise<T>
  }

  get<T>(path: string, params?: Record<string, string | number | undefined>) {
    const query = params
      ? '?' + new URLSearchParams(Object.entries(params).filter(([, v]) => v !== undefined).map(([k, v]) => [k, String(v)])).toString()
      : ''
    return this.request<T>(`${path}${query}`, { method: 'GET' })
  }

  post<T>(path: string, body: unknown) {
    return this.request<T>(path, { method: 'POST', body: JSON.stringify(body) })
  }

  put<T>(path: string, body: unknown) {
    return this.request<T>(path, { method: 'PUT', body: JSON.stringify(body) })
  }

  delete<T>(path: string) {
    return this.request<T>(path, { method: 'DELETE' })
  }
}

export const client = new ApiClient()
