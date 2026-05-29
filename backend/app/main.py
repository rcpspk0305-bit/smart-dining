import time
from collections import defaultdict
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import api_router
from app.services.websocket_manager import manager

# Simple thread-safe in-memory rate limiting store mapping client IP to list of request timestamps
IP_REQUESTS_LOGS = defaultdict(list)

# Initialize FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend web service for the AI-Driven Smart Dining Table Ordering Assistant",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Sliding Window Rate-Limiting Middleware
@app.middleware("http")
async def ip_rate_limiting_middleware(request: Request, call_next):
    # Retrieve client IP address
    client_ip = request.client.host if request.client else "unknown"
    
    # Bypass health check, schema docs, and WebSocket handshakes from rate limiting checks
    if request.url.path in ["/health", "/docs", "/openapi.json", "/redoc"] or "/ws/" in request.url.path:
        return await call_next(request)
        
    now = time.time()
    window_start = now - settings.RATE_LIMIT_WINDOW_SECONDS
    
    # Prune old logs outside the sliding window
    IP_REQUESTS_LOGS[client_ip] = [t for t in IP_REQUESTS_LOGS[client_ip] if t > window_start]
    
    # Enforce request limit checks
    if len(IP_REQUESTS_LOGS[client_ip]) >= settings.RATE_LIMIT_MAX_REQUESTS:
        return JSONResponse(
            status_code=429,
            content={
                "status": "error",
                "error_type": "rate_limit_exceeded",
                "message": "Too many requests. Please slow down and try again later.",
                "retry_after_seconds": int(settings.RATE_LIMIT_WINDOW_SECONDS - (now - IP_REQUESTS_LOGS[client_ip][0]))
            }
        )
        
    IP_REQUESTS_LOGS[client_ip].append(now)
    return await call_next(request)


# Exception handler for Pydantic / FastAPI request payload validation failures
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        # Formulate clean location pathway (e.g. body -> message)
        field = " -> ".join([str(loc) for loc in error["loc"][1:]])
        errors.append({
            "field": field,
            "message": error["msg"],
            "type": error["type"]
        })
    return JSONResponse(
        status_code=422,
        content={
            "status": "error",
            "error_type": "request_validation_failed",
            "message": "The request payload did not pass validation checks. Please inspect inputs.",
            "details": errors
        }
    )


# Exception handler for standard unhandled core system exceptions
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    print(f"CRITICAL ERROR: Unhandled Core Exception in path '{request.url.path}': {str(exc)}")
    import traceback
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "error_type": "internal_server_error",
            "message": "An unexpected server-side error occurred. Gourmet AI Cafe support has been paged."
        }
    )


# Set up CORS middleware to support local frontend compilation/testing
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Register main API router
app.include_router(api_router, prefix=settings.API_STR)


@app.websocket("/api/ws/table/{table_id}")
async def table_websocket_endpoint(websocket: WebSocket, table_id: str):
    """
    WebSocket endpoint establishing persistent connections by tableId.
    Enables instant frothed sync for shared ordering sessions.
    """
    await manager.connect(table_id, websocket)
    try:
        while True:
            # Keep socket open and receive heartbeat ticks
            data = await websocket.receive_text()
            await websocket.send_json({"event": "pong", "data": data})
    except WebSocketDisconnect:
        await manager.disconnect(table_id, websocket)


@app.get("/health", tags=["Health"])
def health_check():
    """
    Fast service diagnostics endpoint.
    """
    return {
        "status": "online",
        "project": settings.PROJECT_NAME,
        "version": "1.0.0"
    }
