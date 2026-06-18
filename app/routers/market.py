"""
Market data router — OHLCV, quotes, trades for equity, index, forex, crypto, commodity.
"""

from fastapi import APIRouter, HTTPException, Query
from app.schemas.common import ApiResponse
from app.services import vnstock_service as vs
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/market", tags=["Market Data"])


@router.get("/quote", response_model=ApiResponse, summary="Bảng giá toàn thị trường")
async def market_quote(symbols: str = Query("", description="Danh sách mã chứng khoán cần lấy bảng giá, cách nhau bởi dấu phẩy. Để trống để lấy rổ VN30.")):
    """Lấy bảng giá real-time toàn thị trường hoặc danh sách các mã chỉ định."""
    try:
        data = vs.get_market_quote(symbols=symbols)
        return ApiResponse(data=data, count=len(data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/equity/{symbol}/ohlcv", response_model=ApiResponse, summary="OHLCV cổ phiếu")
async def equity_ohlcv(
    symbol: str,
    start: str = Query("", description="Ngày bắt đầu YYYY-MM-DD"),
    end: str = Query("", description="Ngày kết thúc YYYY-MM-DD"),
    interval: str = Query("1D", description="Khung thời gian: 1m, 5m, 15m, 30m, 1H, 1D, 1W, 1M"),
    length: int = Query(90, ge=1, le=5000, description="Số nến (nếu không dùng start/end)"),
):
    """Lấy dữ liệu OHLCV lịch sử cho mã cổ phiếu."""
    try:
        data = vs.get_equity_ohlcv(symbol, start=start, end=end, interval=interval, length=length)
        return ApiResponse(data=data, count=len(data), message=f"OHLCV for {symbol.upper()}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/equity/{symbol}/quote", response_model=ApiResponse, summary="Quote real-time cổ phiếu")
async def equity_quote(symbol: str):
    """Lấy bảng giá real-time cho mã cổ phiếu."""
    try:
        data = vs.get_equity_quote(symbol)
        return ApiResponse(data=data, count=len(data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/equity/{symbol}/trades", response_model=ApiResponse, summary="Dữ liệu khớp lệnh tick-by-tick")
async def equity_trades(symbol: str):
    """Lấy dữ liệu giao dịch khớp lệnh theo từng tick."""
    try:
        data = vs.get_equity_trades(symbol)
        return ApiResponse(data=data, count=len(data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/index/{index}/ohlcv", response_model=ApiResponse, summary="OHLCV chỉ số thị trường")
async def index_ohlcv(
    index: str,
    start: str = Query("", description="Ngày bắt đầu"),
    end: str = Query("", description="Ngày kết thúc"),
    interval: str = Query("1D", description="Khung thời gian"),
    length: int = Query(90, ge=1, le=5000),
):
    """Lấy dữ liệu OHLCV cho chỉ số thị trường (VNIndex, HNXIndex, UPCOM)."""
    try:
        data = vs.get_index_ohlcv(index, start=start, end=end, interval=interval, length=length)
        return ApiResponse(data=data, count=len(data), message=f"Index OHLCV for {index.upper()}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/forex/{pair}/ohlcv", response_model=ApiResponse, summary="OHLCV ngoại hối")
async def forex_ohlcv(
    pair: str,
    start: str = Query("", description="Ngày bắt đầu"),
    end: str = Query("", description="Ngày kết thúc"),
    interval: str = Query("1D", description="Khung thời gian"),
    length: int = Query(90, ge=1, le=5000),
):
    """Lấy dữ liệu OHLCV cho cặp ngoại hối (ví dụ: USDVND, JPYVND)."""
    try:
        data = vs.get_forex_ohlcv(pair, start=start, end=end, interval=interval, length=length)
        return ApiResponse(data=data, count=len(data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/crypto/{pair}/ohlcv", response_model=ApiResponse, summary="OHLCV crypto")
async def crypto_ohlcv(
    pair: str,
    start: str = Query("", description="Ngày bắt đầu"),
    end: str = Query("", description="Ngày kết thúc"),
    interval: str = Query("1D", description="Khung thời gian"),
    length: int = Query(90, ge=1, le=5000),
):
    """Lấy dữ liệu OHLCV cho crypto (ví dụ: BTCUSD, ETHUSD)."""
    try:
        data = vs.get_crypto_ohlcv(pair, start=start, end=end, interval=interval, length=length)
        return ApiResponse(data=data, count=len(data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/commodity/{symbol}/ohlcv", response_model=ApiResponse, summary="OHLCV hàng hóa")
async def commodity_ohlcv(
    symbol: str,
    start: str = Query("", description="Ngày bắt đầu"),
    end: str = Query("", description="Ngày kết thúc"),
    interval: str = Query("1D", description="Khung thời gian"),
    length: int = Query(90, ge=1, le=5000),
):
    """Lấy dữ liệu OHLCV cho hàng hóa (dầu, bạc, v.v.)."""
    try:
        data = vs.get_commodity_ohlcv(symbol, start=start, end=end, interval=interval, length=length)
        return ApiResponse(data=data, count=len(data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
