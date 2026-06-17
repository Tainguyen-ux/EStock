"""
Technical Analysis service.
Pure pandas implementation of common indicators.
"""

import pandas as pd
import numpy as np


def calculate_sma(df: pd.DataFrame, period: int = 20, column: str = "close") -> pd.Series:
    """Simple Moving Average."""
    return df[column].rolling(window=period, min_periods=1).mean()


def calculate_ema(df: pd.DataFrame, period: int = 20, column: str = "close") -> pd.Series:
    """Exponential Moving Average."""
    return df[column].ewm(span=period, adjust=False).mean()


def calculate_rsi(df: pd.DataFrame, period: int = 14, column: str = "close") -> pd.Series:
    """Relative Strength Index (Wilder's smoothing)."""
    delta = df[column].diff()
    gain = delta.where(delta > 0, 0.0)
    loss = (-delta).where(delta < 0, 0.0)
    avg_gain = gain.ewm(alpha=1.0 / period, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1.0 / period, min_periods=period, adjust=False).mean()
    rs = avg_gain / avg_loss
    return 100.0 - (100.0 / (1.0 + rs))


def calculate_macd(df: pd.DataFrame, fast: int = 12, slow: int = 26,
                   signal: int = 9, column: str = "close") -> dict[str, pd.Series]:
    """MACD (Moving Average Convergence Divergence)."""
    ema_fast = df[column].ewm(span=fast, adjust=False).mean()
    ema_slow = df[column].ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    return {"macd": macd_line, "signal": signal_line, "histogram": macd_line - signal_line}


def calculate_bollinger_bands(df: pd.DataFrame, period: int = 20,
                              std_dev: float = 2.0, column: str = "close") -> dict[str, pd.Series]:
    """Bollinger Bands."""
    sma = df[column].rolling(window=period, min_periods=1).mean()
    std = df[column].rolling(window=period, min_periods=1).std()
    return {
        "upper": sma + (std * std_dev),
        "middle": sma,
        "lower": sma - (std * std_dev),
        "bandwidth": ((sma + std * std_dev) - (sma - std * std_dev)) / sma * 100,
    }


def calculate_stochastic(df: pd.DataFrame, k_period: int = 14, d_period: int = 3) -> dict[str, pd.Series]:
    """Stochastic Oscillator (%K, %D)."""
    low_min = df["low"].rolling(window=k_period, min_periods=1).min()
    high_max = df["high"].rolling(window=k_period, min_periods=1).max()
    k = 100.0 * (df["close"] - low_min) / (high_max - low_min)
    d = k.rolling(window=d_period, min_periods=1).mean()
    return {"k": k, "d": d}


def calculate_atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """Average True Range."""
    high, low, close = df["high"], df["low"], df["close"].shift(1)
    tr = pd.concat([high - low, (high - close).abs(), (low - close).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1.0 / period, min_periods=period, adjust=False).mean()


def calculate_all_indicators(df: pd.DataFrame,
                              sma_periods: list[int] | None = None,
                              ema_periods: list[int] | None = None,
                              rsi_period: int = 14,
                              macd_fast: int = 12, macd_slow: int = 26, macd_signal: int = 9,
                              bb_period: int = 20, bb_std: float = 2.0) -> pd.DataFrame:
    """Calculate all technical indicators and add as columns."""
    if sma_periods is None:
        sma_periods = [5, 10, 20, 50, 200]
    if ema_periods is None:
        ema_periods = [12, 26]

    result = df.copy()
    for p in sma_periods:
        result[f"sma_{p}"] = calculate_sma(df, period=p)
    for p in ema_periods:
        result[f"ema_{p}"] = calculate_ema(df, period=p)
    result["rsi"] = calculate_rsi(df, period=rsi_period)
    macd = calculate_macd(df, fast=macd_fast, slow=macd_slow, signal=macd_signal)
    result["macd"] = macd["macd"]
    result["macd_signal"] = macd["signal"]
    result["macd_histogram"] = macd["histogram"]
    bb = calculate_bollinger_bands(df, period=bb_period, std_dev=bb_std)
    result["bb_upper"] = bb["upper"]
    result["bb_middle"] = bb["middle"]
    result["bb_lower"] = bb["lower"]
    stoch = calculate_stochastic(df)
    result["stoch_k"] = stoch["k"]
    result["stoch_d"] = stoch["d"]
    result["atr"] = calculate_atr(df)
    if "volume" in df.columns:
        result["volume_sma_20"] = df["volume"].rolling(window=20, min_periods=1).mean()
        result["volume_ratio"] = df["volume"] / result["volume_sma_20"]
    result = result.replace([np.inf, -np.inf], np.nan)
    return result
