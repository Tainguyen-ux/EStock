"""
Stock screener service.
Implements FA and TA screening logic using vnstock data.
"""

import pandas as pd
import numpy as np
import logging
from typing import Any

from app.services import vnstock_service as vs
from app.services.technical_service import calculate_sma, calculate_rsi, calculate_macd

logger = logging.getLogger(__name__)


def screen_fundamental(
    symbols: list[str],
    pe_max: float | None = None, pe_min: float | None = None,
    pb_max: float | None = None, pb_min: float | None = None,
    roe_min: float | None = None, roa_min: float | None = None,
    gross_margin_min: float | None = None, net_margin_min: float | None = None,
    debt_equity_max: float | None = None,
    revenue_growth_min: float | None = None, profit_growth_min: float | None = None,
    limit: int = 50,
) -> list[dict]:
    """
    Screen stocks by fundamental criteria.
    Fetches ratios for each symbol and filters.
    """
    results = []
    for symbol in symbols:
        try:
            ratios = vs.get_financial_ratios(symbol, period="year")
            if not ratios:
                continue
            latest = ratios[-1]  # Most recent period

            # Apply filters
            if pe_max is not None and latest.get("pe") is not None:
                if latest["pe"] > pe_max:
                    continue
            if pe_min is not None and latest.get("pe") is not None:
                if latest["pe"] < pe_min:
                    continue
            if pb_max is not None and latest.get("pb") is not None:
                if latest["pb"] > pb_max:
                    continue
            if pb_min is not None and latest.get("pb") is not None:
                if latest["pb"] < pb_min:
                    continue
            if roe_min is not None and latest.get("roe") is not None:
                if latest["roe"] < roe_min:
                    continue
            if roa_min is not None and latest.get("roa") is not None:
                if latest["roa"] < roa_min:
                    continue
            if debt_equity_max is not None and latest.get("debtOnEquity") is not None:
                if latest["debtOnEquity"] > debt_equity_max:
                    continue

            results.append({"symbol": symbol, "ratios": latest})
            if len(results) >= limit:
                break
        except Exception as e:
            logger.warning(f"Screener skip {symbol}: {e}")
            continue
    return results


def screen_technical(
    symbols: list[str],
    lookback_days: int = 60,
    ma_cross_up: bool = False,
    ma_cross_down: bool = False,
    above_ma20: bool | None = None,
    above_ma50: bool | None = None,
    rsi_oversold: bool = False,
    rsi_overbought: bool = False,
    rsi_min: float | None = None,
    rsi_max: float | None = None,
    volume_spike: bool = False,
    volume_spike_ratio: float = 2.0,
    macd_cross_up: bool = False,
    limit: int = 50,
) -> list[dict]:
    """
    Screen stocks by technical criteria.
    Fetches price data and calculates indicators for each symbol.
    """
    results = []
    for symbol in symbols:
        try:
            ohlcv = vs.get_equity_ohlcv(symbol, length=lookback_days, interval="1D")
            if not ohlcv or len(ohlcv) < 20:
                continue

            df = pd.DataFrame(ohlcv)
            if "close" not in df.columns:
                continue

            # Calculate indicators
            sma20 = calculate_sma(df, period=20)
            sma50 = calculate_sma(df, period=min(50, len(df)))
            rsi = calculate_rsi(df, period=14)
            macd = calculate_macd(df)
            vol_avg = df["volume"].rolling(window=20, min_periods=1).mean() if "volume" in df.columns else None

            last_close = df["close"].iloc[-1]
            last_rsi = rsi.iloc[-1] if not pd.isna(rsi.iloc[-1]) else None
            last_sma20 = sma20.iloc[-1]
            last_sma50 = sma50.iloc[-1]
            last_volume = df["volume"].iloc[-1] if "volume" in df.columns else 0
            last_vol_avg = vol_avg.iloc[-1] if vol_avg is not None else 0

            # Apply filters
            if ma_cross_up and len(df) >= 2:
                prev_close = df["close"].iloc[-2]
                prev_sma20 = sma20.iloc[-2]
                if not (prev_close <= prev_sma20 and last_close > last_sma20):
                    continue

            if ma_cross_down and len(df) >= 2:
                prev_close = df["close"].iloc[-2]
                prev_sma20 = sma20.iloc[-2]
                if not (prev_close >= prev_sma20 and last_close < last_sma20):
                    continue

            if above_ma20 is True and last_close <= last_sma20:
                continue
            if above_ma20 is False and last_close > last_sma20:
                continue
            if above_ma50 is True and last_close <= last_sma50:
                continue
            if above_ma50 is False and last_close > last_sma50:
                continue

            if rsi_oversold and (last_rsi is None or last_rsi >= 30):
                continue
            if rsi_overbought and (last_rsi is None or last_rsi <= 70):
                continue
            if rsi_min is not None and (last_rsi is None or last_rsi < rsi_min):
                continue
            if rsi_max is not None and (last_rsi is None or last_rsi > rsi_max):
                continue

            if volume_spike and last_vol_avg > 0:
                if last_volume / last_vol_avg < volume_spike_ratio:
                    continue

            if macd_cross_up and len(df) >= 2:
                macd_line = macd["macd"]
                signal_line = macd["signal"]
                if not (macd_line.iloc[-2] <= signal_line.iloc[-2] and macd_line.iloc[-1] > signal_line.iloc[-1]):
                    continue

            results.append({
                "symbol": symbol,
                "close": last_close,
                "sma20": round(last_sma20, 2) if last_sma20 else None,
                "sma50": round(last_sma50, 2) if last_sma50 else None,
                "rsi": round(last_rsi, 2) if last_rsi else None,
                "volume": last_volume,
                "volume_avg_20": round(last_vol_avg, 0) if last_vol_avg else None,
                "volume_ratio": round(last_volume / last_vol_avg, 2) if last_vol_avg and last_vol_avg > 0 else None,
                "macd": round(macd["macd"].iloc[-1], 4) if not pd.isna(macd["macd"].iloc[-1]) else None,
                "macd_signal": round(macd["signal"].iloc[-1], 4) if not pd.isna(macd["signal"].iloc[-1]) else None,
            })
            if len(results) >= limit:
                break
        except Exception as e:
            logger.warning(f"TA Screener skip {symbol}: {e}")
            continue
    return results


def compare_stocks(symbols: list[str], include_price: bool = True,
                   include_fundamental: bool = True, period: str = "90") -> list[dict]:
    """Compare multiple stocks side by side."""
    results = []
    for symbol in symbols:
        entry: dict[str, Any] = {"symbol": symbol}
        try:
            if include_price:
                ohlcv = vs.get_equity_ohlcv(symbol, length=int(period), interval="1D")
                if ohlcv:
                    df = pd.DataFrame(ohlcv)
                    entry["price"] = {
                        "current": df["close"].iloc[-1] if "close" in df.columns else None,
                        "high_period": df["high"].max() if "high" in df.columns else None,
                        "low_period": df["low"].min() if "low" in df.columns else None,
                        "change_pct": round(
                            ((df["close"].iloc[-1] - df["close"].iloc[0]) / df["close"].iloc[0]) * 100, 2
                        ) if "close" in df.columns and len(df) > 1 else None,
                        "avg_volume": round(df["volume"].mean(), 0) if "volume" in df.columns else None,
                    }
            if include_fundamental:
                ratios = vs.get_financial_ratios(symbol, period="year")
                if ratios:
                    entry["fundamental"] = ratios[-1]
        except Exception as e:
            logger.warning(f"Compare skip {symbol}: {e}")
            entry["error"] = str(e)
        results.append(entry)
    return results
