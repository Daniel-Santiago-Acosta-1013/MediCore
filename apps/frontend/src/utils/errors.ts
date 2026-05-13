import type { ApiError } from '@/types'

export function parseApiError(error: unknown): string {
  if (error instanceof Error) {
    try {
      const parsed = JSON.parse(error.message) as ApiError['detail']
      if (Array.isArray(parsed)) {
        return parsed.map((e) => `${e.loc[e.loc.length - 1]}: ${e.msg}`).join('\n')
      }
      return String(parsed)
    } catch {
      return error.message
    }
  }
  return 'Error desconocido. Inténtalo de nuevo.'
}
