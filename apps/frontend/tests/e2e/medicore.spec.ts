import { test, expect } from '@playwright/test'

const uniqueEmail = () => `e2e_${Date.now()}_${Math.random().toString(36).slice(2, 7)}@test.com`

test.describe('MediCore Auth', () => {
  test('registro exitoso redirige al dashboard', async ({ page }) => {
    await page.goto('/register')

    await expect(page.getByRole('heading', { name: 'Crear cuenta' })).toBeVisible()

    await page.getByPlaceholder('Juan Pérez').fill('Usuario E2E')
    await page.getByPlaceholder('tu@email.com').fill(uniqueEmail())
    await page.getByPlaceholder('••••••••').fill('Password123!')
    await page.getByRole('button', { name: 'Registrarse' }).click()

    await expect(page).toHaveURL('/')
    await expect(page.getByRole('heading', { name: 'Dashboard' })).toBeVisible()
    await expect(page.getByText('Usuario E2E')).toBeVisible()
  })

  test('login exitoso redirige al dashboard', async ({ page }) => {
    const email = uniqueEmail()
    await page.goto('/register')
    await page.getByPlaceholder('Juan Pérez').fill('Login Test')
    await page.getByPlaceholder('tu@email.com').fill(email)
    await page.getByPlaceholder('••••••••').fill('Password123!')
    await page.getByRole('button', { name: 'Registrarse' }).click()
    await expect(page).toHaveURL('/')

    await page.getByTitle('Cerrar sesión').click()
    await expect(page).toHaveURL('/login')

    await page.getByPlaceholder('tu@email.com').fill(email)
    await page.getByPlaceholder('••••••••').fill('Password123!')
    await page.getByRole('button', { name: 'Iniciar sesión' }).click()

    await expect(page).toHaveURL('/')
    await expect(page.getByRole('heading', { name: 'Dashboard' })).toBeVisible()
  })

  test('login con credenciales incorrectas muestra error', async ({ page }) => {
    await page.goto('/login')

    await page.getByPlaceholder('tu@email.com').fill('noexiste@test.com')
    await page.getByPlaceholder('••••••••').fill('wrongpass')
    await page.getByRole('button', { name: 'Iniciar sesión' }).click()

    await expect(page.getByText('Error')).toBeVisible()
    await expect(page).toHaveURL('/login')
  })

  test('logout redirige a login', async ({ page }) => {
    const email = uniqueEmail()
    await page.goto('/register')
    await page.getByPlaceholder('Juan Pérez').fill('Logout Test')
    await page.getByPlaceholder('tu@email.com').fill(email)
    await page.getByPlaceholder('••••••••').fill('Password123!')
    await page.getByRole('button', { name: 'Registrarse' }).click()
    await expect(page).toHaveURL('/')

    await page.getByTitle('Cerrar sesión').click()
    await expect(page).toHaveURL('/login')
    await expect(page.getByRole('heading', { name: 'Bienvenido a MediCore' })).toBeVisible()
  })
})

test.describe('MediCore Navigation', () => {
  test.beforeEach(async ({ page }) => {
    const email = uniqueEmail()
    await page.goto('/register')
    await page.getByPlaceholder('Juan Pérez').fill('Nav Test')
    await page.getByPlaceholder('tu@email.com').fill(email)
    await page.getByPlaceholder('••••••••').fill('Password123!')
    await page.getByRole('button', { name: 'Registrarse' }).click()
    await expect(page).toHaveURL('/')
  })

  test('navegar a Usuarios', async ({ page }) => {
    await page.getByRole('link', { name: 'Usuarios' }).click()
    await expect(page).toHaveURL('/users')
    await expect(page.getByRole('heading', { name: 'Usuarios' })).toBeVisible()
  })

  test('navegar a Pacientes', async ({ page }) => {
    await page.getByRole('link', { name: 'Pacientes' }).click()
    await expect(page).toHaveURL('/patients')
    await expect(page.getByRole('heading', { name: 'Pacientes' })).toBeVisible()
  })

  test('navegar a Doctores', async ({ page }) => {
    await page.getByRole('link', { name: 'Doctores' }).click()
    await expect(page).toHaveURL('/doctors')
    await expect(page.getByRole('heading', { name: 'Doctores' })).toBeVisible()
  })

  test('navegar a Citas', async ({ page }) => {
    await page.getByRole('link', { name: 'Citas' }).click()
    await expect(page).toHaveURL('/appointments')
    await expect(page.getByRole('heading', { name: 'Citas' })).toBeVisible()
  })

  test('navegar a Dashboard desde otra página', async ({ page }) => {
    await page.goto('/users')
    await page.getByRole('link', { name: 'Dashboard' }).click()
    await expect(page).toHaveURL('/')
    await expect(page.getByRole('heading', { name: 'Dashboard' })).toBeVisible()
  })
})

test.describe('MediCore Dashboard', () => {
  test.beforeEach(async ({ page }) => {
    const email = uniqueEmail()
    await page.goto('/register')
    await page.getByPlaceholder('Juan Pérez').fill('Dashboard Test')
    await page.getByPlaceholder('tu@email.com').fill(email)
    await page.getByPlaceholder('••••••••').fill('Password123!')
    await page.getByRole('button', { name: 'Registrarse' }).click()
    await expect(page).toHaveURL('/')
  })

  test('muestra estadísticas en el dashboard', async ({ page }) => {
    await expect(page.getByText('Pacientes')).toBeVisible()
    await expect(page.getByText('Doctores')).toBeVisible()
    await expect(page.getByText('Citas hoy')).toBeVisible()
    await expect(page.getByText('Pendientes')).toBeVisible()
  })

  test('muestra acciones rápidas', async ({ page }) => {
    await expect(page.getByRole('link', { name: 'Nueva cita' })).toBeVisible()
    await expect(page.getByRole('link', { name: 'Nuevo paciente' })).toBeVisible()
    await expect(page.getByRole('link', { name: 'Nuevo doctor' })).toBeVisible()
    await expect(page.getByRole('link', { name: 'Ver usuarios' })).toBeVisible()
  })

  test('acción rápida Nueva cita navega a Citas', async ({ page }) => {
    await page.getByRole('link', { name: 'Nueva cita' }).click()
    await expect(page).toHaveURL('/appointments')
  })
})

test.describe('MediCore Usuarios CRUD', () => {
  test.beforeEach(async ({ page }) => {
    const email = uniqueEmail()
    await page.goto('/register')
    await page.getByPlaceholder('Juan Pérez').fill('CRUD Test')
    await page.getByPlaceholder('tu@email.com').fill(email)
    await page.getByPlaceholder('••••••••').fill('Password123!')
    await page.getByRole('button', { name: 'Registrarse' }).click()
    await expect(page).toHaveURL('/')
    await page.goto('/users')
    await expect(page.getByRole('heading', { name: 'Usuarios' })).toBeVisible()
  })

  test('abrir modal de crear usuario', async ({ page }) => {
    await page.getByRole('button', { name: 'Nuevo usuario' }).click()
    await expect(page.getByRole('heading', { name: 'Nuevo usuario' })).toBeVisible()
    await expect(page.getByPlaceholder('Juan Pérez')).toBeVisible()
    await expect(page.getByPlaceholder('tu@email.com')).toBeVisible()
  })

  test('cancelar modal de crear usuario', async ({ page }) => {
    await page.getByRole('button', { name: 'Nuevo usuario' }).click()
    await expect(page.getByRole('heading', { name: 'Nuevo usuario' })).toBeVisible()
    await page.getByRole('button', { name: 'Cancelar' }).click()
    await expect(page.getByRole('heading', { name: 'Nuevo usuario' })).not.toBeVisible()
  })
})

test.describe('MediCore Sidebar', () => {
  test.beforeEach(async ({ page }) => {
    const email = uniqueEmail()
    await page.goto('/register')
    await page.getByPlaceholder('Juan Pérez').fill('Sidebar Test')
    await page.getByPlaceholder('tu@email.com').fill(email)
    await page.getByPlaceholder('••••••••').fill('Password123!')
    await page.getByRole('button', { name: 'Registrarse' }).click()
    await expect(page).toHaveURL('/')
  })

  test('colapsar y expandir sidebar', async ({ page }) => {
    const sidebar = page.locator('.sidebar')
    const toggle = page.locator('.sidebar-toggle')

    await expect(sidebar).not.toHaveClass(/collapsed/)
    await toggle.click()
    await expect(sidebar).toHaveClass(/collapsed/)
    await toggle.click()
    await expect(sidebar).not.toHaveClass(/collapsed/)
  })

  test('sidebar colapsado solo muestra iconos', async ({ page }) => {
    await page.locator('.sidebar-toggle').click()
    await expect(page.locator('.sidebar.collapsed')).toBeVisible()
    await expect(page.locator('.sidebar.collapsed .sidebar-title')).not.toBeVisible()
  })
})

test.describe('MediCore Protected Routes', () => {
  test('acceder a / sin autenticación redirige a login', async ({ page }) => {
    await page.goto('/')
    await expect(page).toHaveURL('/login')
  })

  test('acceder a /users sin autenticación redirige a login', async ({ page }) => {
    await page.goto('/users')
    await expect(page).toHaveURL('/login')
  })

  test('acceder a /patients sin autenticación redirige a login', async ({ page }) => {
    await page.goto('/patients')
    await expect(page).toHaveURL('/login')
  })

  test('acceder a /login estando autenticado redirige a dashboard', async ({ page }) => {
    const email = uniqueEmail()
    await page.goto('/register')
    await page.getByPlaceholder('Juan Pérez').fill('Redirect Test')
    await page.getByPlaceholder('tu@email.com').fill(email)
    await page.getByPlaceholder('••••••••').fill('Password123!')
    await page.getByRole('button', { name: 'Registrarse' }).click()
    await expect(page).toHaveURL('/')

    await page.goto('/login')
    await expect(page).toHaveURL('/')
  })
})
