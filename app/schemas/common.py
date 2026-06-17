"""
Common Pydantic schemas for API responses.
"""

from pydantic import BaseModel, Field
from typing import Any
from datetime import datetime


class ApiResponse(BaseModel):
    """Standard API response wrapper."""
    success: bool = True
    data: Any = None
    message: str = ""
    timestamp: datetime = Field(default_factory=datetime.now)
    count: int | None = None


class ErrorResponse(BaseModel):
    """Error response schema."""
    success: bool = False
    error: str
    detail: str = ""
    timestamp: datetime = Field(default_factory=datetime.now)


class PaginationParams(BaseModel):
    """Common pagination parameters."""
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=50, ge=1, le=500)
