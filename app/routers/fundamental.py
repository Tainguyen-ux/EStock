"""
Fundamental data router — Financial reports and ratios.
"""

from fastapi import APIRouter, HTTPException, Query
from app.schemas.common import ApiResponse
from app.services import vnstock_service as vs
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/fundamental", tags=["Fundamental Data"])


@router.get("/{symbol}/balance-sheet", response_model=ApiResponse, summary="Bảng cân đối kế toán")
async def balance_sheet(
    symbol: str,
    period: str = Query("year", description="Kỳ báo cáo: year hoặc quarter"),
):
    """Lấy bảng cân đối kế toán."""
    try:
        data = vs.get_balance_sheet(symbol, period=period)
        return ApiResponse(data=data, count=len(data), message=f"Balance sheet for {symbol.upper()} ({period})")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{symbol}/income-statement", response_model=ApiResponse, summary="Kết quả HĐKD")
async def income_statement(
    symbol: str,
    period: str = Query("year", description="Kỳ báo cáo: year hoặc quarter"),
):
    """Lấy báo cáo kết quả hoạt động kinh doanh."""
    try:
        data = vs.get_income_statement(symbol, period=period)
        return ApiResponse(data=data, count=len(data), message=f"Income statement for {symbol.upper()} ({period})")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{symbol}/cash-flow", response_model=ApiResponse, summary="Lưu chuyển tiền tệ")
async def cash_flow(
    symbol: str,
    period: str = Query("year", description="Kỳ báo cáo: year hoặc quarter"),
):
    """Lấy báo cáo lưu chuyển tiền tệ."""
    try:
        data = vs.get_cash_flow(symbol, period=period)
        return ApiResponse(data=data, count=len(data), message=f"Cash flow for {symbol.upper()} ({period})")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{symbol}/ratios", response_model=ApiResponse, summary="Chỉ số tài chính")
async def financial_ratios(
    symbol: str,
    period: str = Query("year", description="Kỳ báo cáo: year hoặc quarter"),
):
    """Lấy các chỉ số tài chính (P/E, P/B, ROE, ROA, EPS, ...)."""
    try:
        data = vs.get_financial_ratios(symbol, period=period)
        return ApiResponse(data=data, count=len(data), message=f"Financial ratios for {symbol.upper()} ({period})")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
