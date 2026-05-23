import time
from typing import Callable

from fastapi import Request, Response
from prometheus_client import Counter, Gauge, Histogram


api_errors_total = Counter(
    "medicore_api_errors_total",
    "HTTP error responses returned by the API.",
    ["module", "endpoint", "status_code", "error_type"],
)

api_exceptions_total = Counter(
    "medicore_api_exceptions_total",
    "Unhandled exceptions raised by the API.",
    ["module", "exception_type"],
)

auth_failures_total = Counter(
    "medicore_auth_failures_total",
    "Authentication failures by reason.",
    ["reason"],
)

permission_denied_total = Counter(
    "medicore_permission_denied_total",
    "Authorization denials by role and endpoint.",
    ["role", "endpoint"],
)

db_errors_total = Counter(
    "medicore_db_errors_total",
    "Database operation failures.",
    ["module", "operation", "error_type"],
)

db_operation_duration_seconds = Histogram(
    "medicore_db_operation_duration_seconds",
    "Database operation duration.",
    ["module", "operation"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10),
)

external_dependency_up = Gauge(
    "medicore_external_dependency_up",
    "External dependency health.",
    ["dependency"],
)

frontend_errors_total = Counter(
    "medicore_frontend_errors_total",
    "Frontend errors reported by the browser.",
    ["route", "source", "error_type"],
)

frontend_api_errors_total = Counter(
    "medicore_frontend_api_errors_total",
    "API errors observed by the frontend.",
    ["route", "method", "status_code"],
)

frontend_api_request_duration_seconds = Histogram(
    "medicore_frontend_api_request_duration_seconds",
    "API request duration observed by the frontend.",
    ["route", "method"],
    buckets=(0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10, 30),
)

frontend_toasts_total = Counter(
    "medicore_frontend_toasts_total",
    "Toast notifications shown in the frontend.",
    ["type"],
)


def initialize_metric_series() -> None:
    """Expose zero-valued custom series so Grafana does not show empty panels."""
    for status_code, error_type in (
        ("400", "client"),
        ("401", "auth"),
        ("403", "permission"),
        ("404", "not_found"),
        ("422", "validation"),
        ("500", "server"),
    ):
        api_errors_total.labels(
            module="api",
            endpoint="none",
            status_code=status_code,
            error_type=error_type,
        )

    for module in ("api", "auth", "database"):
        api_exceptions_total.labels(module=module, exception_type="none")

    for reason in (
        "invalid_credentials",
        "inactive_user",
        "invalid_token",
        "invalid_token_user_not_found",
        "missing_token",
    ):
        auth_failures_total.labels(reason=reason)

    for role in ("ADMIN", "DOCTOR", "NURSE", "RECEPTIONIST", "BILLING", "PATIENT", "anonymous"):
        permission_denied_total.labels(role=role, endpoint="role_guard")

    for operation in ("connect", "query", "transaction"):
        db_errors_total.labels(module="database", operation=operation, error_type="none")

    db_operation_duration_seconds.labels(module="database", operation="connect")
    external_dependency_up.labels(dependency="database").set(0)

    for source in ("api", "render", "network", "auth", "unhandled", "promise", "toast"):
        frontend_errors_total.labels(route="/", source=source, error_type="none")

    for method in ("GET", "POST", "PUT", "DELETE"):
        for status_code in ("0", "400", "401", "403", "404", "422", "500"):
            frontend_api_errors_total.labels(route="/", method=method, status_code=status_code)

    for toast_type in ("error", "success", "warning", "info"):
        frontend_toasts_total.labels(type=toast_type)


def route_template(request: Request) -> str:
    route = request.scope.get("route")
    path = getattr(route, "path", request.url.path)
    return str(path)


def module_from_path(path: str) -> str:
    parts = [part for part in path.split("/") if part]
    if not parts:
        return "root"
    return parts[0].replace("-", "_")


def error_type_for_status(status_code: int) -> str:
    if status_code == 401:
        return "auth"
    if status_code == 403:
        return "permission"
    if status_code == 404:
        return "not_found"
    if status_code == 422:
        return "validation"
    if status_code >= 500:
        return "server"
    return "client"


async def collect_api_error_metrics(request: Request, call_next: Callable) -> Response:
    try:
        response = await call_next(request)
    except Exception as exc:
        endpoint = route_template(request)
        module = module_from_path(endpoint)
        api_exceptions_total.labels(module=module, exception_type=type(exc).__name__).inc()
        raise

    if response.status_code >= 400:
        endpoint = route_template(request)
        module = module_from_path(endpoint)
        api_errors_total.labels(
            module=module,
            endpoint=endpoint,
            status_code=str(response.status_code),
            error_type=error_type_for_status(response.status_code),
        ).inc()

    return response


def observe_db_operation(module: str, operation: str, func: Callable):
    start = time.perf_counter()
    try:
        return func()
    except Exception as exc:
        db_errors_total.labels(module=module, operation=operation, error_type=type(exc).__name__).inc()
        external_dependency_up.labels(dependency="database").set(0)
        raise
    finally:
        db_operation_duration_seconds.labels(module=module, operation=operation).observe(time.perf_counter() - start)


initialize_metric_series()
