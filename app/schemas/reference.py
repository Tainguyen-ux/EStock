"""
Reference data schemas.
"""

from pydantic import BaseModel, Field


class CompanySearchParams(BaseModel):
    """Parameters for company/symbol search."""
    query: str = Field(..., min_length=1, description="Search query (symbol or company name)")


class EquityListParams(BaseModel):
    """Parameters for equity listing filters."""
    group: str = Field(default="", description="Group code (e.g., VN30, HNX30)")
    exchange: str = Field(default="", description="Exchange (HOSE, HNX, UPCOM)")
    industry: str = Field(default="", description="Industry code")
