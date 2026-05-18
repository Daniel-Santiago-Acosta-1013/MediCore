export interface User {
  id: string;
  email: string;
  full_name: string;
  role: 'ADMIN' | 'DOCTOR' | 'NURSE' | 'RECEPTIONIST' | 'BILLING' | 'PATIENT';
  is_active: boolean;
  created_at: string;
}

export interface UserRegister {
  email: string;
  full_name: string;
  password: string;
  role?: User['role'];
}

export interface UserCreate extends UserRegister {}

export interface Token {
  access_token: string;
  token_type: string;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface Patient {
  id: string;
  user_id: string | null;
  date_of_birth: string | null;
  phone: string | null;
  address: string | null;
  emergency_contact_name: string | null;
  emergency_contact_phone: string | null;
  created_at: string;
}

export interface Doctor {
  id: string;
  user_id: string;
  full_name: string;
  license_number: string;
  specialty: string;
  phone: string | null;
  created_at: string;
}

export interface Appointment {
  id: string;
  patient_id: string;
  doctor_id: string;
  appointment_date: string;
  status: 'SCHEDULED' | 'COMPLETED' | 'CANCELLED';
  notes: string | null;
  created_at: string;
}

export interface MedicalRecord {
  id: string;
  patient_id: string;
  doctor_id: string | null;
  appointment_id: string | null;
  diagnosis: string | null;
  treatment: string | null;
  notes: string | null;
  created_at: string;
}

export interface MedicalOrder {
  id: string;
  medical_record_id: string;
  order_type: string;
  status: 'PENDING' | 'COMPLETED' | 'CANCELLED';
  doctor_id: string | null;
  created_at: string;
}

export interface Invoice {
  id: string;
  patient_id: string;
  appointment_id: string | null;
  amount: number;
  status: 'PENDING' | 'PAID' | 'OVERDUE';
  due_date: string | null;
  paid_at: string | null;
  created_at: string;
}

export interface AuditLog {
  id: string;
  table_name: string;
  record_id: string;
  action: string;
  old_data: unknown;
  new_data: unknown;
  performed_by: string | null;
  created_at: string;
}

export interface ApiError {
  detail: string | Array<{ loc: string[]; msg: string; type: string }>;
}

export interface ListParams {
  limit?: number;
  offset?: number;
  [key: string]: string | number | undefined;
}
