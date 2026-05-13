from fastapi import FastAPI
from app.modules.auth.router import router as auth_router
from app.modules.users.router import router as users_router
from app.modules.patients.router import router as patients_router
from app.modules.doctors.router import router as doctors_router
from app.modules.appointments.router import router as appointments_router
from app.modules.medical_records.router import router as medical_records_router
from app.modules.medical_orders.router import router as medical_orders_router
from app.modules.billing.router import router as billing_router
from app.modules.audit.router import router as audit_router

app = FastAPI(title="MediCore API", version="0.1.0")

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(patients_router)
app.include_router(doctors_router)
app.include_router(appointments_router)
app.include_router(medical_records_router)
app.include_router(medical_orders_router)
app.include_router(billing_router)
app.include_router(audit_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
