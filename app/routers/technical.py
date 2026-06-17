"""
Technical Analysis router — Indicators calculated on OHLCV data.
"""

from fastapi import APIRouter, HTTPException, Query
from app.schemas.common import ApiResponse
from app.services import vnstock_service as vs
from app.services import technical_service as ta
import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/technical", tags=["Technical Analysis"])


def _get_ohlcv_df(symbol: str, length: int = 200) -> pd.DataFrame:
    """Helper to get OHLCV data as DataFrame."""
    data = vs.get_equity_ohlcv(symbol, length=length, interval="1D")
    if not data:
        raise ValueError(f"No OHLCV data for {symbol}")
    df = pd.DataFrame(data)
    # Ensure numeric columns
    for col in ["open", "high", "low", "close", "volume"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def _series_to_records(df: pd.DataFrame, indicator_cols: list[str]) -> list[dict]:
    """Convert DataFrame with indicator columns to records, replacing NaN with None."""
    cols = ["time"] + [c for c in indicator_cols if c in df.columns]
    if "close" not in cols and "close" in df.columns:
        cols.insert(1, "close")
    result = df[cols].copy()
    result = result.replace([np.inf, -np.inf], np.nan)
    result = result.where(pd.notnull(result), None)
    # Convert datetime
    for col in result.columns:
        if pd.api.types.is_datetime64_any_dtype(result[col]):
            result[col] = result[col].dt.strftime("%Y-%m-%d")
    return result.to_dict(orient="records")


@router.get("/{symbol}/indicators", response_model=ApiResponse, summary="Tất cả chỉ báo kỹ thuật")
async def all_indicators(
    symbol: str,
    length: int = Query(200, ge=30, le=5000, description="Số phiên lịch sử"),
    sma_periods: str = Query("5,10,20,50,200", description="Chu kỳ SMA (phân cách bằng dấu phẩy)"),
    ema_periods: str = Query("12,26", description="Chu kỳ EMA (phân cách bằng dấu phẩy)"),
    rsi_period: int = Query(14, ge=2, le=50, description="Chu kỳ RSI"),
):
    """
    Tính toán tất cả chỉ báo kỹ thuật cho mã cổ phiếu:
    SMA, EMA, RSI, MACD, Bollinger Bands, Stochastic, ATR, Volume ratio.
    """
    try:
        df = _get_ohlcv_df(symbol, length)
        sma_list = [int(x.strip()) for x in sma_periods.split(",") if x.strip()]
        ema_list = [int(x.strip()) for x in ema_periods.split(",") if x.strip()]

        result = ta.calculate_all_indicators(
            df, sma_periods=sma_list, ema_periods=ema_list, rsi_period=rsi_period
        )
        records = vs.df_to_records(result)
        return ApiResponse(data=records, count=len(records), message=f"All indicators for {symbol.upper()}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{symbol}/sma", response_model=ApiResponse, summary="Simple Moving Average")
async def sma(
    symbol: str,
    period: int = Query(20, ge=2, le=500, description="Chu kỳ SMA"),
    length: int = Query(100, ge=10, le=5000, description="Số phiên lịch sử"),
):
    """Tính Simple Moving Average (SMA)."""
    try:
        df = _get_ohlcv_df(symbol, length)
        df["sma"] = ta.calculate_sma(df, period=period)
        records = _series_to_records(df, ["sma"])
        return ApiResponse(data=records, count=len(records), message=f"SMA({period}) for {symbol.upper()}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{symbol}/ema", response_model=ApiResponse, summary="Exponential Moving Average")
async def ema(
    symbol: str,
    period: int = Query(20, ge=2, le=500, description="Chu kỳ EMA"),
    length: int = Query(100, ge=10, le=5000, description="Số phiên lịch sử"),
):
    """Tính Exponential Moving Average (EMA)."""
    try:
        df = _get_ohlcv_df(symbol, length)
        df["ema"] = ta.calculate_ema(df, period=period)
        records = _series_to_records(df, ["ema"])
        return ApiResponse(data=records, count=len(records), message=f"EMA({period}) for {symbol.upper()}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{symbol}/rsi", response_model=ApiResponse, summary="Relative Strength Index")
async def rsi(
    symbol: str,
    period: int = Query(14, ge=2, le=50, description="Chu kỳ RSI"),
    length: int = Query(100, ge=20, le=5000, description="Số phiên lịch sử"),
):
    """Tính Relative Strength Index (RSI)."""
    try:
        df = _get_ohlcv_df(symbol, length)
        df["rsi"] = ta.calculate_rsi(df, period=period)
        records = _series_to_records(df, ["rsi"])
        return ApiResponse(data=records, count=len(records), message=f"RSI({period}) for {symbol.upper()}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{symbol}/macd", response_model=ApiResponse, summary="MACD")
async def macd(
    symbol: str,
    fast: int = Query(12, ge=2, description="Chu kỳ nhanh"),
    slow: int = Query(26, ge=2, description="Chu kỳ chậm"),
    signal: int = Query(9, ge=2, description="Chu kỳ signal"),
    length: int = Query(100, ge=30, le=5000, description="Số phiên lịch sử"),
):
    """Tính MACD (Moving Average Convergence Divergence)."""
    try:
        df = _get_ohlcv_df(symbol, length)
        macd_data = ta.calculate_macd(df, fast=fast, slow=slow, signal=signal)
        df["macd"] = macd_data["macd"]
        df["macd_signal"] = macd_data["signal"]
        df["macd_histogram"] = macd_data["histogram"]
        records = _series_to_records(df, ["macd", "macd_signal", "macd_histogram"])
        return ApiResponse(data=records, count=len(records),
                           message=f"MACD({fast},{slow},{signal}) for {symbol.upper()}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{symbol}/bollinger", response_model=ApiResponse, summary="Bollinger Bands")
async def bollinger(
    symbol: str,
    period: int = Query(20, ge=2, le=200, description="Chu kỳ"),
    std_dev: float = Query(2.0, ge=0.5, le=4.0, description="Hệ số độ lệch chuẩn"),
    length: int = Query(100, ge=20, le=5000, description="Số phiên lịch sử"),
):
    """Tính Bollinger Bands."""
    try:
        df = _get_ohlcv_df(symbol, length)
        bb = ta.calculate_bollinger_bands(df, period=period, std_dev=std_dev)
        df["bb_upper"] = bb["upper"]
        df["bb_middle"] = bb["middle"]
        df["bb_lower"] = bb["lower"]
        df["bb_bandwidth"] = bb["bandwidth"]
        records = _series_to_records(df, ["bb_upper", "bb_middle", "bb_lower", "bb_bandwidth"])
        return ApiResponse(data=records, count=len(records),
                           message=f"Bollinger({period},{std_dev}) for {symbol.upper()}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{symbol}/stochastic", response_model=ApiResponse, summary="Stochastic Oscillator")
async def stochastic(
    symbol: str,
    k_period: int = Query(14, ge=2, description="Chu kỳ %K"),
    d_period: int = Query(3, ge=2, description="Chu kỳ %D"),
    length: int = Query(100, ge=20, le=5000, description="Số phiên lịch sử"),
):
    """Tính Stochastic Oscillator (%K, %D)."""
    try:
        df = _get_ohlcv_df(symbol, length)
        stoch = ta.calculate_stochastic(df, k_period=k_period, d_period=d_period)
        df["stoch_k"] = stoch["k"]
        df["stoch_d"] = stoch["d"]
        records = _series_to_records(df, ["stoch_k", "stoch_d"])
        return ApiResponse(data=records, count=len(records),
                           message=f"Stochastic({k_period},{d_period}) for {symbol.upper()}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{symbol}/atr", response_model=ApiResponse, summary="Average True Range")
async def atr(
    symbol: str,
    period: int = Query(14, ge=2, le=50, description="Chu kỳ ATR"),
    length: int = Query(100, ge=20, le=5000, description="Số phiên lịch sử"),
):
    """Tính Average True Range (ATR)."""
    try:
        df = _get_ohlcv_df(symbol, length)
        df["atr"] = ta.calculate_atr(df, period=period)
        records = _series_to_records(df, ["atr"])
        return ApiResponse(data=records, count=len(records), message=f"ATR({period}) for {symbol.upper()}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
