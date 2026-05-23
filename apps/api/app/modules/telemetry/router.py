from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.core.metrics import (
    frontend_api_errors_total,
    frontend_api_request_duration_seconds,
    frontend_errors_total,
    frontend_toasts_total,
)


router = APIRouter(prefix="/telemetry", tags=["telemetry"])


class FrontendErrorEvent(BaseModel):
    route: str = Field(default="/", max_length=120)
    source: Literal["api", "render", "network", "auth", "unhandled", "promise", "toast"] = "unhandled"
    error_type: str = Field(default="unknown", max_length=80)


class FrontendApiEvent(BaseModel):
    route: str = Field(default="/", max_length=120)
    method: str = Field(default="GET", max_length=12)
    status_code: int = Field(ge=0, le=599)
    duration_ms: float = Field(ge=0)


class FrontendToastEvent(BaseModel):
    type: Literal["error", "success", "warning", "info"]


@router.post("/frontend-error", status_code=204)
def record_frontend_error(event: FrontendErrorEvent):
    frontend_errors_total.labels(
        route=event.route,
        source=event.source,
        error_type=event.error_type,
    ).inc()


@router.post("/frontend-api", status_code=204)
def record_frontend_api(event: FrontendApiEvent):
    method = event.method.upper()
    frontend_api_request_duration_seconds.labels(route=event.route, method=method).observe(event.duration_ms / 1000)
    if event.status_code >= 400 or event.status_code == 0:
        frontend_api_errors_total.labels(
            route=event.route,
            method=method,
            status_code=str(event.status_code),
        ).inc()


@router.post("/frontend-toast", status_code=204)
def record_frontend_toast(event: FrontendToastEvent):
    frontend_toasts_total.labels(type=event.type).inc()

