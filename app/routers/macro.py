"""
Macro data router — Gold prices, exchange rates, forex.
"""

from fastapi import APIRouter, HTTPException, Query
from app.schemas.common import ApiResponse
from app.services import vnstock_service as vs
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/macro", tags=["Macro Data"])


@router.get("/gold", response_model=ApiResponse, summary="Giá vàng")
async def gold_prices(source: str = Query("sjc", description="Nguồn giá vàng: sjc, doji, pnj")):
    """Lấy giá vàng trong nước (SJC, DOJI, PNJ)."""
    try:
        data = vs.get_gold_prices(source=source)
        return ApiResponse(data=data, count=len(data), message=f"Gold prices from {source.upper()}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/exchange-rate", response_model=ApiResponse, summary="Tỷ giá ngoại tệ")
async def exchange_rates():
    """Lấy tỷ giá ngoại tệ từ Vietcombank."""
    try:
        data = vs.get_exchange_rates()
        return ApiResponse(data=data, count=len(data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/forex/{pair}/ohlcv", response_model=ApiResponse, summary="Lịch sử tỷ giá ngoại hối")
async def forex_history(
    pair: str,
    start: str = Query("", description="Ngày bắt đầu YYYY-MM-DD"),
    end: str = Query("", description="Ngày kết thúc YYYY-MM-DD"),
    interval: str = Query("1D", description="Khung thời gian"),
    length: int = Query(90, ge=1, le=5000),
):
    """Lấy dữ liệu OHLCV lịch sử cho cặp ngoại hối (ví dụ: USDVND, EURVND)."""
    try:
        data = vs.get_forex_ohlcv(pair, start=start, end=end, interval=interval, length=length)
        return ApiResponse(data=data, count=len(data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
