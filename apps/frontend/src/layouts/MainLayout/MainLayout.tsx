import { useState } from 'react'
import { Outlet } from 'react-router-dom'
import { Sidebar } from '@/components/Sidebar/Sidebar'
import { Header } from '@/components/Header/Header'
import './MainLayout.css'

export function MainLayout() {
  const [collapsed, setCollapsed] = useState(false)
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  return (
    <div className="app-layout">
      <Sidebar
        collapsed={collapsed}
        mobileMenuOpen={mobileMenuOpen}
        onToggle={() => setCollapsed(!collapsed)}
        onCloseMobile={() => setMobileMenuOpen(false)}
      />
      <div className={`main-content ${collapsed ? 'collapsed' : ''}`}>
        <Header onMenuToggle={() => setMobileMenuOpen(true)} />
        <main className="page-content">
          <Outlet />
        </main>
      </div>
      {mobileMenuOpen && (
        <div className="mobile-overlay" onClick={() => setMobileMenuOpen(false)} />
      )}
    </div>
  )
}
