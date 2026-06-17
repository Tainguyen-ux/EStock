"""
Funds router — Mutual fund data.
"""

from fastapi import APIRouter, HTTPException
from app.schemas.common import ApiResponse
from app.services import vnstock_service as vs
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/funds", tags=["Investment Funds"])


@router.get("/list", response_model=ApiResponse, summary="Danh sách quỹ mở")
async def fund_list():
    """Lấy danh sách tất cả quỹ đầu tư mở."""
    try:
        data = vs.get_fund_list()
        return ApiResponse(data=data, count=len(data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{fund_code}/nav", response_model=ApiResponse, summary="Lịch sử NAV")
async def fund_nav(fund_code: str):
    """Lấy lịch sử giá trị tài sản ròng (NAV) của quỹ."""
    try:
        data = vs.get_fund_nav(fund_code)
        return ApiResponse(data=data, count=len(data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{fund_code}/top-holding", response_model=ApiResponse, summary="Top nắm giữ")
async def fund_top_holding(fund_code: str):
    """Lấy danh sách cổ phiếu nắm giữ lớn nhất của quỹ."""
    try:
        data = vs.get_fund_top_holding(fund_code)
        return ApiResponse(data=data, count=len(data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{fund_code}/industry-holding", response_model=ApiResponse, summary="Phân bổ ngành")
async def fund_industry_holding(fund_code: str):
    """Lấy phân bổ đầu tư theo ngành của quỹ."""
    try:
        data = vs.get_fund_industry_holding(fund_code)
        return ApiResponse(data=data, count=len(data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{fund_code}/asset-holding", response_model=ApiResponse, summary="Phân bổ tài sản")
async def fund_asset_holding(fund_code: str):
    """Lấy phân bổ đầu tư theo loại tài sản của quỹ."""
    try:
        data = vs.get_fund_asset_holding(fund_code)
        return ApiResponse(data=data, count=len(data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
