from common.errors.schemas import ProblemDetail
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.exceptions import (
    DataSourceError,
    InvalidVersionError,
    OSLError,
    TableNotFoundError,
)

PROBLEM_RESPONSES: dict[int | str, dict[str, object]] = {
    422: {
        "model": ProblemDetail,
        "description": (
            "Validation failure — invalid version, malformed query parameter, "
            "or unsupported value."
        ),
    },
    404: {
        "model": ProblemDetail,
        "description": (
            "The requested table does not exist for the given server/version."
        ),
    },
    503: {
        "model": ProblemDetail,
        "description": "HuggingFace or DuckDB upstream is unavailable.",
    },
}


def _problem(status: int, title: str, detail: str, instance: str) -> JSONResponse:
    body = ProblemDetail(
        type=f"about:blank#{title.lower().replace(' ', '-')}",
        title=title,
        status=status,
        detail=detail,
        instance=instance,
    ).model_dump()
    return JSONResponse(
        status_code=status,
        content=body,
        media_type="application/problem+json",
    )


async def _invalid_version(request: Request, exc: InvalidVersionError) -> JSONResponse:
    return _problem(
        status=422,
        title="Invalid version",
        detail=(
            f"Version '{exc.version}' is not available for server '{exc.server}'. "
            f"Available versions: {', '.join(exc.available)}."
        ),
        instance=str(request.url),
    )


async def _table_not_found(request: Request, exc: TableNotFoundError) -> JSONResponse:
    return _problem(
        status=404,
        title="Table not found",
        detail=(
            f"Table '{exc.table}' does not exist for server '{exc.server}' "
            f"version '{exc.version}'."
        ),
        instance=str(request.url),
    )


async def _datasource_error(request: Request, exc: DataSourceError) -> JSONResponse:
    return _problem(
        status=503,
        title="Data source unavailable",
        detail=exc.detail,
        instance=str(request.url),
    )


async def _unhandled_osl(request: Request, exc: OSLError) -> JSONResponse:
    return _problem(
        status=500,
        title="Internal error",
        detail=str(exc),
        instance=str(request.url),
    )


async def _validation_error(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    parts = []
    for err in exc.errors():
        loc = ".".join(str(p) for p in err.get("loc", [])[1:]) or "request"
        parts.append(f"{loc}: {err.get('msg', 'invalid value')}")
    summary = "; ".join(parts) or "Request validation failed."
    return _problem(
        status=422,
        title="Validation error",
        detail=summary,
        instance=str(request.url),
    )


def register(app: FastAPI) -> None:
    app.add_exception_handler(RequestValidationError, _validation_error)  # type: ignore[arg-type]
    app.add_exception_handler(InvalidVersionError, _invalid_version)
    app.add_exception_handler(TableNotFoundError, _table_not_found)
    app.add_exception_handler(DataSourceError, _datasource_error)
    app.add_exception_handler(OSLError, _unhandled_osl)
