"""
Common API response schemas.

Every endpoint returns either:
  - APIResponse  (single-object or status)
  - PaginatedResponse  (list endpoint)
"""

from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel

DataT = TypeVar("DataT")


class APIResponse(BaseModel):
    """Standard success / failure response."""

    success: bool = True
    message: str = "Operation completed"
    data: Optional[Any] = None


class PaginatedResponse(BaseModel):
    """Standard paginated list response."""

    items: list
    total: int
    page: int
    page_size: int
    total_pages: int


