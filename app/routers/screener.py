"""
Stock screener router — FA and TA filtering, stock comparison.
"""

from fastapi import APIRouter, HTTPException
from app.schemas.common import ApiResponse
from app.schemas.screener import FAScreenerParams, TAScreenerParams, CompareParams
from app.services import vnstock_service as vs
from app.services import screener_service as screener
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/screener", tags=["Stock Screener"])


def _get_symbol_list(exchange: str = "", group: str = "", symbols: list[str] | None = None) -> list[str]:
    """Helper to resolve symbol list from exchange/group/explicit list."""
    if symbols:
        return [s.upper() for s in symbols]
    try:
        if group:
            data = vs.get_equity_by_group(group)
        elif exchange:
            data = vs.get_equity_by_exchange(exchange)
        else:
            data = vs.get_equity_by_group("VN30")  # Default to VN30

        # Extract symbol column
        if data:
            for key in ["symbol", "ticker", "code", "stock_code"]:
                if key in data[0]:
                    return [item[key] for item in data if item.get(key)]
        return []
    except Exception as e:
        logger.error(f"Failed to get symbol list: {e}")
        return []


@router.post("/fundamental", response_model=ApiResponse, summary="Lọc cổ phiếu theo phân tích cơ bản")
async def screen_by_fundamental(params: FAScreenerParams):
    """
    Bộ lọc cổ phiếu FA (Fundamental Analysis).

    Tìm cổ phiếu theo các tiêu chí:
    - **Định giá**: P/E, P/B
    - **Hiệu suất**: ROE, ROA, biên lợi nhuận
    - **Đòn bẩy**: Nợ/Vốn CSH
    - **Tăng trưởng**: Tăng trưởng doanh thu, lợi nhuận
    """
    try:
        symbols = _get_symbol_list(params.exchange, params.group)
        if not symbols:
            return ApiResponse(data=[], count=0, message="No symbols found for the given filter")

        results = screener.screen_fundamental(
            symbols=symbols,
            pe_max=params.pe_max, pe_min=params.pe_min,
            pb_max=params.pb_max, pb_min=params.pb_min,
            roe_min=params.roe_min, roa_min=params.roa_min,
            gross_margin_min=params.gross_margin_min,
            net_margin_min=params.net_margin_min,
            debt_equity_max=params.debt_equity_max,
            revenue_growth_min=params.revenue_growth_min,
            profit_growth_min=params.profit_growth_min,
            limit=params.limit,
        )
        return ApiResponse(data=results, count=len(results), message=f"Screened {len(symbols)} symbols")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/technical", response_model=ApiResponse, summary="Lọc cổ phiếu theo phân tích kỹ thuật")
async def screen_by_technical(params: TAScreenerParams):
    """
    Bộ lọc cổ phiếu TA (Technical Analysis).

    Tìm cổ phiếu theo các tiêu chí:
    - **Moving Average**: Cắt lên/xuống MA20, trên/dưới MA20/MA50
    - **RSI**: Quá bán (<30), quá mua (>70), hoặc khoảng RSI tùy chỉnh
    - **Khối lượng**: Đột biến khối lượng so với trung bình 20 phiên
    - **MACD**: MACD cắt lên signal line
    """
    try:
        symbols = _get_symbol_list(params.exchange, params.group, params.symbols)
        if not symbols:
            return ApiResponse(data=[], count=0, message="No symbols found for the given filter")

        results = screener.screen_technical(
            symbols=symbols,
            lookback_days=params.lookback_days,
            ma_cross_up=params.ma_cross_up,
            ma_cross_down=params.ma_cross_down,
            above_ma20=params.above_ma20,
            above_ma50=params.above_ma50,
            rsi_oversold=params.rsi_oversold,
            rsi_overbought=params.rsi_overbought,
            rsi_min=params.rsi_min,
            rsi_max=params.rsi_max,
            volume_spike=params.volume_spike,
            volume_spike_ratio=params.volume_spike_ratio,
            macd_cross_up=params.macd_cross_up,
            limit=params.limit,
        )
        return ApiResponse(data=results, count=len(results), message=f"Screened {len(symbols)} symbols")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/compare", response_model=ApiResponse, summary="So sánh nhiều mã cổ phiếu")
async def compare_stocks(params: CompareParams):
    """
    So sánh nhiều mã cổ phiếu side-by-side.

    Bao gồm dữ liệu giá và chỉ số tài chính cơ bản.
    """
    try:
        results = screener.compare_stocks(
            symbols=params.symbols,
            include_price=params.include_price,
            include_fundamental=params.include_fundamental,
            period=params.period,
        )
        return ApiResponse(data=results, count=len(results))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
