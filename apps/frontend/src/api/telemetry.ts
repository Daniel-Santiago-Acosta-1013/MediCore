const API_BASE = import.meta.env.VITE_API_URL || '/api'

type ErrorSource = 'api' | 'render' | 'network' | 'auth' | 'unhandled' | 'promise' | 'toast'
type ToastType = 'error' | 'success' | 'warning' | 'info'

function currentRoute() {
  return window.location.pathname || '/'
}

function postTelemetry(path: string, payload: unknown) {
  const body = JSON.stringify(payload)
  const url = `${API_BASE}${path}`

  if (navigator.sendBeacon) {
    const blob = new Blob([body], { type: 'application/json' })
    navigator.sendBeacon(url, blob)
    return
  }

  void fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body,
    keepalive: true,
  }).catch(() => undefined)
}

export function reportFrontendError(source: ErrorSource, errorType = 'unknown', route = currentRoute()) {
  postTelemetry('/telemetry/frontend-error', {
    route,
    source,
    error_type: errorType,
  })
}

export function reportFrontendApi(method: string, statusCode: number, durationMs: number, route = currentRoute()) {
  postTelemetry('/telemetry/frontend-api', {
    route,
    method,
    status_code: statusCode,
    duration_ms: durationMs,
  })
}

export function reportFrontendToast(type: ToastType) {
  postTelemetry('/telemetry/frontend-toast', { type })
}

export function installGlobalErrorTelemetry() {
  window.addEventListener('error', (event) => {
    reportFrontendError('unhandled', event.error?.name || 'Error')
  })

  window.addEventListener('unhandledrejection', (event) => {
    const reason = event.reason
    const errorType = reason instanceof Error ? reason.name : 'UnhandledPromiseRejection'
    reportFrontendError('promise', errorType)
  })
}
