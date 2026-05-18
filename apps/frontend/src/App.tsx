import { AppRoutes } from '@/routes'
import { ToastProvider } from '@/stores/ToastContext'

function App() {
  return (
    <ToastProvider>
      <AppRoutes />
    </ToastProvider>
  )
}

export default App
