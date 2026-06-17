"""
Fundamental data schemas.
"""

from pydantic import BaseModel, Field
from typing import Literal


class FinancialReportParams(BaseModel):
    """Parameters for financial report requests."""
    period: Literal["year", "quarter"] = Field(default="year", description="Report period")
    lang: Literal["vi", "en"] = Field(default="vi", description="Language for column names")
