"""
Vnstock service wrapper.
Handles DataFrame → JSON conversion, error handling, and caching.
"""

import pandas as pd
import logging
from datetime import datetime, timedelta
from typing import Any

from app.dependencies import get_market, get_reference, get_fundamental, get_retail
from app.config import get_settings
from app.utils.cache import cached

logger = logging.getLogger(__name__)
settings = get_settings()


def df_to_records(df: Any) -> list[dict]:
    """Convert DataFrame to list of dicts, handling NaN and datetime."""
    if df is None:
        return []
    if isinstance(df, dict):
        return [df]
    if isinstance(df, pd.DataFrame):
        if df.empty:
            return []
        # Convert datetime columns to ISO string
        for col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = df[col].dt.strftime("%Y-%m-%d %H:%M:%S")
        # Replace NaN with None
        df = df.where(pd.notnull(df), None)
        return df.to_dict(orient="records")
    if isinstance(df, pd.Series):
        return [df.to_dict()]
    return []


def safe_call(func, *args, **kwargs) -> Any:
    """Safely call a vnstock function with error handling."""
    try:
        result = func(*args, **kwargs)
        return result
    except Exception as e:
        logger.error(f"Vnstock API error: {func.__name__} - {e}")
        raise


# ═══════════════════════════════════════════════════════════════
# MARKET DATA
# ═══════════════════════════════════════════════════════════════

def get_equity_ohlcv(symbol: str, start: str = "", end: str = "",
                     interval: str = "1D", length: int = 90) -> list[dict]:
    """Get historical OHLCV data for an equity symbol."""
    market = get_market()
    equity = market.equity(symbol.upper())
    kwargs = {"interval": interval}
    if start and end:
        kwargs["start"] = start
        kwargs["end"] = end
    else:
        kwargs["length"] = length
    df = safe_call(equity.ohlcv, **kwargs)
    return df_to_records(df)


def get_equity_quote(symbol: str) -> list[dict]:
    """Get real-time quote for an equity symbol."""
    market = get_market()
    equity = market.equity(symbol.upper())
    df = safe_call(equity.quote)
    return df_to_records(df)


def get_equity_trades(symbol: str) -> list[dict]:
    """Get tick-by-tick trade data."""
    market = get_market()
    equity = market.equity(symbol.upper())
    df = safe_call(equity.trades)
    return df_to_records(df)


def get_market_quote(symbols: str | list[str] = "") -> list[dict]:
    """Get market quote for a list of symbols or a comma-separated string.
    If no symbols are specified, defaults to VN30 constituents."""
    market = get_market()
    
    if not symbols:
        try:
            ref = get_reference()
            vn30_series = ref.equity.list_by_group(group="VN30")
            symbols = vn30_series.tolist()
        except Exception as e:
            logger.warning(f"Failed to fetch VN30 list: {e}. Falling back to default list.")
            symbols = ["FPT", "TCB", "VCB", "HPG", "VNM", "MWG", "VIC", "VHM", "SSI", "STB"]
    elif isinstance(symbols, str):
        symbols = [s.strip().upper() for s in symbols.split(",") if s.strip()]
        
    if not symbols:
        return []
        
    df = safe_call(market.quote, symbol=symbols)
    return df_to_records(df)


def get_index_ohlcv(index: str, start: str = "", end: str = "",
                    interval: str = "1D", length: int = 90) -> list[dict]:
    """Get OHLCV data for a market index."""
    market = get_market()
    idx = market.index(index.upper())
    kwargs = {"interval": interval}
    if start and end:
        kwargs["start"] = start
        kwargs["end"] = end
    else:
        kwargs["length"] = length
    df = safe_call(idx.ohlcv, **kwargs)
    return df_to_records(df)


def get_forex_ohlcv(pair: str, start: str = "", end: str = "",
                    interval: str = "1D", length: int = 90) -> list[dict]:
    """Get OHLCV data for a forex pair."""
    market = get_market()
    fx = market.forex(pair.upper())
    kwargs = {"interval": interval}
    if start and end:
        kwargs["start"] = start
        kwargs["end"] = end
    else:
        kwargs["length"] = length
    df = safe_call(fx.ohlcv, **kwargs)
    return df_to_records(df)


def get_crypto_ohlcv(pair: str, start: str = "", end: str = "",
                     interval: str = "1D", length: int = 90) -> list[dict]:
    """Get OHLCV data for a crypto pair."""
    market = get_market()
    crypto = market.crypto(pair.upper())
    kwargs = {"interval": interval}
    if start and end:
        kwargs["start"] = start
        kwargs["end"] = end
    else:
        kwargs["length"] = length
    df = safe_call(crypto.ohlcv, **kwargs)
    return df_to_records(df)


def get_commodity_ohlcv(symbol: str, start: str = "", end: str = "",
                        interval: str = "1D", length: int = 90) -> list[dict]:
    """Get OHLCV data for a commodity."""
    market = get_market()
    commodity = market.commodity(symbol.upper())
    kwargs = {"interval": interval}
    if start and end:
        kwargs["start"] = start
        kwargs["end"] = end
    else:
        kwargs["length"] = length
    df = safe_call(commodity.ohlcv, **kwargs)
    return df_to_records(df)


# ═══════════════════════════════════════════════════════════════
# DERIVATIVES DATA
# ═══════════════════════════════════════════════════════════════

def get_futures_ohlcv(symbol: str, start: str = "", end: str = "",
                      interval: str = "1D", length: int = 90) -> list[dict]:
    """Get OHLCV data for a futures contract."""
    market = get_market()
    futures = market.futures(symbol.upper())
    kwargs = {"interval": interval}
    if start and end:
        kwargs["start"] = start
        kwargs["end"] = end
    else:
        kwargs["length"] = length
    df = safe_call(futures.ohlcv, **kwargs)
    return df_to_records(df)


def get_futures_quote(symbol: str) -> list[dict]:
    """Get real-time quote for futures."""
    market = get_market()
    futures = market.futures(symbol.upper())
    df = safe_call(futures.quote)
    return df_to_records(df)


def get_futures_trades(symbol: str) -> list[dict]:
    """Get tick-by-tick trades for futures."""
    market = get_market()
    futures = market.futures(symbol.upper())
    df = safe_call(futures.trades)
    return df_to_records(df)


def get_warrant_ohlcv(symbol: str, start: str = "", end: str = "",
                      interval: str = "1D", length: int = 90) -> list[dict]:
    """Get OHLCV data for a covered warrant."""
    market = get_market()
    warrant = market.warrant(symbol.upper())
    kwargs = {"interval": interval}
    if start and end:
        kwargs["start"] = start
        kwargs["end"] = end
    else:
        kwargs["length"] = length
    df = safe_call(warrant.ohlcv, **kwargs)
    return df_to_records(df)


def get_warrant_quote(symbol: str) -> list[dict]:
    """Get real-time quote for warrants."""
    market = get_market()
    warrant = market.warrant(symbol.upper())
    df = safe_call(warrant.quote)
    return df_to_records(df)


def get_etf_ohlcv(symbol: str, start: str = "", end: str = "",
                  interval: str = "1D", length: int = 90) -> list[dict]:
    """Get OHLCV data for an ETF."""
    market = get_market()
    etf = market.etf(symbol.upper())
    kwargs = {"interval": interval}
    if start and end:
        kwargs["start"] = start
        kwargs["end"] = end
    else:
        kwargs["length"] = length
    df = safe_call(etf.ohlcv, **kwargs)
    return df_to_records(df)


def get_etf_quote(symbol: str) -> list[dict]:
    """Get real-time quote for ETF."""
    market = get_market()
    etf = market.etf(symbol.upper())
    df = safe_call(etf.quote)
    return df_to_records(df)


# ═══════════════════════════════════════════════════════════════
# FUND DATA
# ═══════════════════════════════════════════════════════════════

def get_fund_nav(fund_code: str) -> list[dict]:
    """Get fund NAV history."""
    market = get_market()
    fund = market.fund(fund_code)
    df = safe_call(fund.nav)
    return df_to_records(df)


def get_fund_top_holding(fund_code: str) -> list[dict]:
    """Get fund top holdings."""
    market = get_market()
    fund = market.fund(fund_code)
    df = safe_call(fund.top_holding)
    return df_to_records(df)


def get_fund_industry_holding(fund_code: str) -> list[dict]:
    """Get fund industry allocation."""
    market = get_market()
    fund = market.fund(fund_code)
    df = safe_call(fund.industry_holding)
    return df_to_records(df)


def get_fund_asset_holding(fund_code: str) -> list[dict]:
    """Get fund asset allocation."""
    market = get_market()
    fund = market.fund(fund_code)
    df = safe_call(fund.asset_holding)
    return df_to_records(df)


# ═══════════════════════════════════════════════════════════════
# REFERENCE DATA
# ═══════════════════════════════════════════════════════════════

def get_equity_list() -> list[dict]:
    """Get all equity symbols."""
    ref = get_reference()
    df = safe_call(ref.equity.list)
    return df_to_records(df)


def get_equity_by_group(group: str) -> list[dict]:
    """Get equities by group (e.g., VN30)."""
    ref = get_reference()
    df = safe_call(ref.equity.list_by_group, group=group)
    return df_to_records(df)


def get_equity_by_industry() -> list[dict]:
    """Get equities grouped by industry."""
    ref = get_reference()
    df = safe_call(ref.equity.list_by_industry)
    return df_to_records(df)


def get_equity_by_exchange(exchange: str) -> list[dict]:
    """Get equities by exchange."""
    ref = get_reference()
    df = safe_call(ref.equity.list_by_exchange)
    if isinstance(df, pd.DataFrame) and not df.empty and "exchange" in df.columns:
        df = df[df["exchange"].astype(str).str.upper() == exchange.upper()]
    return df_to_records(df)


def get_company_info(symbol: str) -> list[dict]:
    """Get company overview."""
    ref = get_reference()
    company = ref.company(symbol.upper())
    df = safe_call(company.info)
    return df_to_records(df)


def get_company_shareholders(symbol: str) -> list[dict]:
    """Get major shareholders."""
    ref = get_reference()
    company = ref.company(symbol.upper())
    df = safe_call(company.shareholders)
    return df_to_records(df)


def get_company_officers(symbol: str) -> list[dict]:
    """Get company officers/leadership."""
    ref = get_reference()
    company = ref.company(symbol.upper())
    df = safe_call(company.officers)
    return df_to_records(df)


def get_company_subsidiaries(symbol: str) -> list[dict]:
    """Get subsidiaries."""
    ref = get_reference()
    company = ref.company(symbol.upper())
    df = safe_call(company.subsidiaries)
    return df_to_records(df)


def get_company_insider_trading(symbol: str) -> list[dict]:
    """Get insider trading history."""
    ref = get_reference()
    company = ref.company(symbol.upper())
    df = safe_call(company.insider_trading)
    return df_to_records(df)


def get_company_news(symbol: str) -> list[dict]:
    """Get company related news."""
    ref = get_reference()
    company = ref.company(symbol.upper())
    df = safe_call(company.news)
    return df_to_records(df)


def get_company_events(symbol: str) -> list[dict]:
    """Get corporate events."""
    ref = get_reference()
    company = ref.company(symbol.upper())
    df = safe_call(company.events)
    return df_to_records(df)


def get_company_ownership(symbol: str) -> list[dict]:
    """Get ownership structure."""
    ref = get_reference()
    company = ref.company(symbol.upper())
    df = safe_call(company.ownership)
    return df_to_records(df)


def get_company_capital_history(symbol: str) -> list[dict]:
    """Get capital change history."""
    ref = get_reference()
    company = ref.company(symbol.upper())
    df = safe_call(company.capital_history)
    return df_to_records(df)


def get_index_list() -> list[dict]:
    """Get all market indices."""
    ref = get_reference()
    df = safe_call(ref.index.list)
    return df_to_records(df)


def get_index_members(index: str) -> list[dict]:
    """Get index constituents."""
    ref = get_reference()
    df = safe_call(ref.index.members, index=index)
    return df_to_records(df)


def get_index_groups() -> list[dict]:
    """Get supported index groups."""
    ref = get_reference()
    df = safe_call(ref.index.groups)
    return df_to_records(df)


def get_index_info() -> list[dict]:
    """Get all market indices metadata."""
    ref = get_reference()
    df = safe_call(ref.index.info)
    return df_to_records(df)


def get_industry_list() -> list[dict]:
    """Get ICB industry classification."""
    ref = get_reference()
    df = safe_call(ref.industry.list)
    return df_to_records(df)


def get_industry_sectors() -> list[dict]:
    """Get symbols grouped by industry."""
    ref = get_reference()
    df = safe_call(ref.industry.sectors)
    return df_to_records(df)


def search_symbol(query: str) -> list[dict]:
    """Search for symbols."""
    ref = get_reference()
    df = safe_call(ref.search.symbol, query=query)
    return df_to_records(df)


def search_info(query: str) -> list[dict]:
    """Search for detailed asset information."""
    ref = get_reference()
    df = safe_call(ref.search.info, query=query)
    return df_to_records(df)


def get_market_status() -> Any:
    """Get live market status."""
    ref = get_reference()
    result = safe_call(ref.market.status)
    if isinstance(result, dict):
        return result
    return df_to_records(result)


def get_etf_list() -> list[dict]:
    """Get all ETFs."""
    ref = get_reference()
    df = safe_call(ref.etf.list)
    return df_to_records(df)


def get_futures_list() -> list[dict]:
    """Get all futures instruments."""
    ref = get_reference()
    df = safe_call(ref.futures.list)
    return df_to_records(df)


def get_futures_info() -> Any:
    """Get futures specifications."""
    ref = get_reference()
    result = safe_call(ref.futures.info)
    if isinstance(result, dict):
        return result
    return df_to_records(result)


def get_warrant_list() -> list[dict]:
    """Get all covered warrants."""
    ref = get_reference()
    df = safe_call(ref.warrant.list)
    return df_to_records(df)


def get_warrant_info() -> Any:
    """Get warrant specifications."""
    ref = get_reference()
    result = safe_call(ref.warrant.info)
    if isinstance(result, dict):
        return result
    return df_to_records(result)


def get_bond_list() -> list[dict]:
    """Get all bonds."""
    ref = get_reference()
    df = safe_call(ref.bond.list)
    return df_to_records(df)


def get_fund_list() -> list[dict]:
    """Get all mutual funds."""
    ref = get_reference()
    df = safe_call(ref.fund.list)
    return df_to_records(df)


def get_fund_ref_top_holding(fund_code: str) -> list[dict]:
    """Get fund top holdings (reference)."""
    ref = get_reference()
    df = safe_call(ref.fund.top_holding, fund_code=fund_code)
    return df_to_records(df)


def get_fund_ref_nav_report(fund_code: str) -> list[dict]:
    """Get fund NAV report (reference)."""
    ref = get_reference()
    df = safe_call(ref.fund.nav_report, fund_code=fund_code)
    return df_to_records(df)


# ═══════════════════════════════════════════════════════════════
# FUNDAMENTAL DATA
# ═══════════════════════════════════════════════════════════════

def get_balance_sheet(symbol: str, period: str = "year") -> list[dict]:
    """Get balance sheet."""
    fund = get_fundamental()
    equity = fund.equity(symbol.upper())
    df = safe_call(equity.balance_sheet, period=period)
    return df_to_records(df)


def get_income_statement(symbol: str, period: str = "year") -> list[dict]:
    """Get income statement."""
    fund = get_fundamental()
    equity = fund.equity(symbol.upper())
    df = safe_call(equity.income_statement, period=period)
    return df_to_records(df)


def get_cash_flow(symbol: str, period: str = "year") -> list[dict]:
    """Get cash flow statement."""
    fund = get_fundamental()
    equity = fund.equity(symbol.upper())
    df = safe_call(equity.cash_flow, period=period)
    return df_to_records(df)


def get_financial_ratios(symbol: str, period: str = "year") -> list[dict]:
    """Get financial ratios."""
    fund = get_fundamental()
    equity = fund.equity(symbol.upper())
    df = safe_call(equity.ratios, period=period)
    return df_to_records(df)


# ═══════════════════════════════════════════════════════════════
# RETAIL DATA (Gold, Exchange Rate)
# ═══════════════════════════════════════════════════════════════

def get_gold_prices(source: str = "sjc") -> list[dict]:
    """Get gold prices."""
    retail = get_retail()
    df = safe_call(retail.gold, source=source)
    return df_to_records(df)


def get_exchange_rates() -> list[dict]:
    """Get VCB exchange rates."""
    retail = get_retail()
    df = safe_call(retail.exchange_rate)
    return df_to_records(df)
