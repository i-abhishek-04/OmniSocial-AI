"""
Application entrypoint: FastAPI app instance, router registration,
middleware wiring, and startup handlers.
"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.config import get_settings
from app.core.database import init_db
from app.core.logging import configure_logging
from app.middleware.cors import configure_cors
from app.routers import auth, users, analytics, chat, inbox, scheduler
from app.utils.exceptions import AppError
from app.utils.helpers import error_response

settings = get_settings()

configure_logging()

app = FastAPI(title=settings.APP_NAME)

configure_cors(app)


@app.exception_handler(AppError)
def handle_app_error(request: Request, exc: AppError):
    return JSONResponse(status_code=exc.status_code, content=error_response(exc.message))


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
def root():
    return {"status": "ok", "service": settings.APP_NAME}


@app.get("/health")
def health():
    return {"status": "healthy"}


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(analytics.router)
app.include_router(chat.router)
app.include_router(inbox.router)
app.include_router(scheduler.router)

