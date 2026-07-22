"""
Structured request logging middleware.

Logs every request:
  - Method
  - URL path
  - Authenticated user (if any)
  - Execution time
  - HTTP status code
"""

import logging
import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("rcms.access")
logger.setLevel(logging.INFO)

# Ensure a console handler exists
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )
    logger.addHandler(handler)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware that logs method, URL, user, duration, and status."""

    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        duration = time.perf_counter() - start

        # Extract username from request state (set by auth dependency)
        username = getattr(request.state, "username", "anonymous")

        logger.info(
            "method=%(method)s path=%(path)s user=%(user)s "
            "status=%(status)d duration=%(duration).3fs",
            {
                "method": request.method,
                "path": request.url.path,
                "user": username,
                "status": response.status_code,
                "duration": duration,
            },
        )
        return response


