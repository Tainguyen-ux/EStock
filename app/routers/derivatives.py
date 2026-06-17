"""
Derivatives router — Futures, warrants, ETFs.
"""

from fastapi import APIRouter, HTTPException, Query
from app.schemas.common import ApiResponse
from app.services import vnstock_service as vs
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/derivatives", tags=["Derivatives"])


# ── Futures ─────────────────────────────────────────────────

@router.get("/futures/list", response_model=ApiResponse, summary="Danh sách hợp đồng tương lai")
async def futures_list():
    """Lấy danh sách tất cả hợp đồng tương lai."""
    try:
        data = vs.get_futures_list()
        return ApiResponse(data=data, count=len(data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/futures/info", response_model=ApiResponse, summary="Thông tin phái sinh")
async def futures_info():
    """Lấy thông số kỹ thuật hợp đồng tương lai."""
    try:
        data = vs.get_futures_info()
        return ApiResponse(data=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/futures/{symbol}/ohlcv", response_model=ApiResponse, summary="OHLCV futures")
async def futures_ohlcv(
    symbol: str,
    start: str = Query("", description="Ngày bắt đầu"),
    end: str = Query("", description="Ngày kết thúc"),
    interval: str = Query("1D", description="Khung thời gian"),
    length: int = Query(90, ge=1, le=5000),
):
    """Lấy dữ liệu OHLCV cho hợp đồng tương lai (VN30F1M, VN30F2M, ...)."""
    try:
        data = vs.get_futures_ohlcv(symbol, start=start, end=end, interval=interval, length=length)
        return ApiResponse(data=data, count=len(data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/futures/{symbol}/quote", response_model=ApiResponse, summary="Quote futures")
async def futures_quote(symbol: str):
    """Lấy bảng giá real-time cho futures."""
    try:
        data = vs.get_futures_quote(symbol)
        return ApiResponse(data=data, count=len(data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/futures/{symbol}/trades", response_model=ApiResponse, summary="Trades futures")
async def futures_trades(symbol: str):
    """Lấy dữ liệu tick-by-tick cho futures."""
    try:
        data = vs.get_futures_trades(symbol)
        return ApiResponse(data=data, count=len(data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Warrants ────────────────────────────────────────────────

@router.get("/warrants/list", response_model=ApiResponse, summary="Danh sách chứng quyền")
async def warrant_list():
    """Lấy danh sách tất cả chứng quyền có bảo đảm."""
    try:
        data = vs.get_warrant_list()
        return ApiResponse(data=data, count=len(data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/warrants/info", response_model=ApiResponse, summary="Thông tin chứng quyền")
async def warrant_info():
    """Lấy thông số kỹ thuật chứng quyền."""
    try:
        data = vs.get_warrant_info()
        return ApiResponse(data=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/warrants/{symbol}/ohlcv", response_model=ApiResponse, summary="OHLCV chứng quyền")
async def warrant_ohlcv(
    symbol: str,
    start: str = Query("", description="Ngày bắt đầu"),
    end: str = Query("", description="Ngày kết thúc"),
    interval: str = Query("1D", description="Khung thời gian"),
    length: int = Query(90, ge=1, le=5000),
):
    """Lấy dữ liệu OHLCV cho chứng quyền."""
    try:
        data = vs.get_warrant_ohlcv(symbol, start=start, end=end, interval=interval, length=length)
        return ApiResponse(data=data, count=len(data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/warrants/{symbol}/quote", response_model=ApiResponse, summary="Quote chứng quyền")
async def warrant_quote(symbol: str):
    """Lấy bảng giá real-time cho chứng quyền."""
    try:
        data = vs.get_warrant_quote(symbol)
        return ApiResponse(data=data, count=len(data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── ETF ─────────────────────────────────────────────────────

@router.get("/etf/list", response_model=ApiResponse, summary="Danh sách ETF")
async def etf_list():
    """Lấy danh sách tất cả ETF."""
    try:
        data = vs.get_etf_list()
        return ApiResponse(data=data, count=len(data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/etf/{symbol}/ohlcv", response_model=ApiResponse, summary="OHLCV ETF")
async def etf_ohlcv(
    symbol: str,
    start: str = Query("", description="Ngày bắt đầu"),
    end: str = Query("", description="Ngày kết thúc"),
    interval: str = Query("1D", description="Khung thời gian"),
    length: int = Query(90, ge=1, le=5000),
):
    """Lấy dữ liệu OHLCV cho ETF."""
    try:
        data = vs.get_etf_ohlcv(symbol, start=start, end=end, interval=interval, length=length)
        return ApiResponse(data=data, count=len(data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/etf/{symbol}/quote", response_model=ApiResponse, summary="Quote ETF")
async def etf_quote(symbol: str):
    """Lấy bảng giá real-time cho ETF."""
    try:
        data = vs.get_etf_quote(symbol)
        return ApiResponse(data=data, count=len(data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
