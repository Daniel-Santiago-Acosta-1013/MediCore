import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuth } from '@/stores/AuthContext'
import { Loading } from '@/components/Loading/Loading'
import { MainLayout } from '@/layouts/MainLayout/MainLayout'
import { AuthLayout } from '@/layouts/AuthLayout/AuthLayout'
import { Login } from '@/pages/Login/Login'
import { Register } from '@/pages/Register/Register'
import { Dashboard } from '@/pages/Dashboard/Dashboard'
import { Users } from '@/pages/Users/Users'
import { Patients } from '@/pages/Patients/Patients'
import { Doctors } from '@/pages/Doctors/Doctors'
import { Appointments } from '@/pages/Appointments/Appointments'
import { NotFound } from '@/pages/NotFound/NotFound'
import { AccessDenied } from '@/pages/AccessDenied/AccessDenied'
import type { User } from '@/types'

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, isLoading } = useAuth()

  if (isLoading) {
    return <Loading />
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  return <>{children}</>
}

function PublicRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, isLoading } = useAuth()

  if (isLoading) {
    return <Loading />
  }

  if (isAuthenticated) {
    return <Navigate to="/" replace />
  }

  return <>{children}</>
}

function RoleRoute({
  children,
  allowedRoles,
}: {
  children: React.ReactNode
  allowedRoles: User['role'][]
}) {
  const { user, isLoading } = useAuth()

  if (isLoading) {
    return <Loading />
  }

  if (!user || !allowedRoles.includes(user.role)) {
    return <AccessDenied />
  }

  return <>{children}</>
}

export function AppRoutes() {
  return (
    <Routes>
      <Route element={<AuthLayout />}>
        <Route
          path="/login"
          element={
            <PublicRoute>
              <Login />
            </PublicRoute>
          }
        />
        <Route
          path="/register"
          element={
            <PublicRoute>
              <Register />
            </PublicRoute>
          }
        />
      </Route>

      <Route
        element={
          <ProtectedRoute>
            <MainLayout />
          </ProtectedRoute>
        }
      >
        <Route path="/" element={<Dashboard />} />
        <Route
          path="/users"
          element={
            <RoleRoute allowedRoles={['ADMIN']}>
              <Users />
            </RoleRoute>
          }
        />
        <Route
          path="/patients"
          element={
            <RoleRoute allowedRoles={['ADMIN', 'DOCTOR', 'NURSE', 'RECEPTIONIST', 'BILLING']}>
              <Patients />
            </RoleRoute>
          }
        />
        <Route
          path="/doctors"
          element={
            <RoleRoute allowedRoles={['ADMIN', 'DOCTOR', 'NURSE', 'RECEPTIONIST', 'BILLING']}>
              <Doctors />
            </RoleRoute>
          }
        />
        <Route
          path="/appointments"
          element={
            <RoleRoute allowedRoles={['ADMIN', 'DOCTOR', 'NURSE', 'RECEPTIONIST', 'BILLING', 'PATIENT']}>
              <Appointments />
            </RoleRoute>
          }
        />
      </Route>

      <Route path="*" element={<NotFound />} />
    </Routes>
  )
}
