import { useState } from 'react'
import { Outlet } from 'react-router-dom'
import { Sidebar } from '@/components/Sidebar/Sidebar'
import { Header } from '@/components/Header/Header'
import './MainLayout.css'

export function MainLayout() {
  const [collapsed, setCollapsed] = useState(false)

  return (
    <div className="app-layout">
      <Sidebar collapsed={collapsed} onToggle={() => setCollapsed(!collapsed)} />
      <div className={`main-content ${collapsed ? 'collapsed' : ''}`}>
        <Header />
        <main className="page-content">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
