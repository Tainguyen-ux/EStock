"""
Reference data router — listings, company info, indices, industries, search.
"""

from fastapi import APIRouter, HTTPException, Query
from app.schemas.common import ApiResponse
from app.services import vnstock_service as vs
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/reference", tags=["Reference Data"])


# ── Equity Listing ──────────────────────────────────────────

@router.get("/equity/list", response_model=ApiResponse, summary="Danh sách tất cả mã cổ phiếu")
async def equity_list():
    """Lấy danh sách tất cả mã cổ phiếu niêm yết."""
    try:
        data = vs.get_equity_list()
        return ApiResponse(data=data, count=len(data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/equity/by-group", response_model=ApiResponse, summary="Danh sách mã theo nhóm")
async def equity_by_group(group: str = Query("VN30", description="Mã nhóm: VN30, HNX30, VNMidCap, etc.")):
    """Lấy danh sách mã cổ phiếu theo nhóm (VN30, HNX30, VNMidCap, ...)."""
    try:
        data = vs.get_equity_by_group(group)
        return ApiResponse(data=data, count=len(data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/equity/by-industry", response_model=ApiResponse, summary="Danh sách mã theo ngành")
async def equity_by_industry():
    """Lấy danh sách mã cổ phiếu phân theo ngành ICB."""
    try:
        data = vs.get_equity_by_industry()
        return ApiResponse(data=data, count=len(data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/equity/by-exchange", response_model=ApiResponse, summary="Danh sách mã theo sàn")
async def equity_by_exchange(exchange: str = Query("HOSE", description="Sàn: HOSE, HNX, UPCOM")):
    """Lấy danh sách mã cổ phiếu theo sàn giao dịch."""
    try:
        data = vs.get_equity_by_exchange(exchange)
        return ApiResponse(data=data, count=len(data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Company Info ────────────────────────────────────────────

@router.get("/company/{symbol}/info", response_model=ApiResponse, summary="Thông tin tổng quan công ty")
async def company_info(symbol: str):
    """Lấy thông tin tổng quan doanh nghiệp."""
    try:
        data = vs.get_company_info(symbol)
        return ApiResponse(data=data, count=len(data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/company/{symbol}/shareholders", response_model=ApiResponse, summary="Cổ đông lớn")
async def company_shareholders(symbol: str):
    """Lấy danh sách cổ đông lớn."""
    try:
        data = vs.get_company_shareholders(symbol)
        return ApiResponse(data=data, count=len(data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/company/{symbol}/officers", response_model=ApiResponse, summary="Ban lãnh đạo")
async def company_officers(symbol: str):
    """Lấy danh sách ban lãnh đạo."""
    try:
        data = vs.get_company_officers(symbol)
        return ApiResponse(data=data, count=len(data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/company/{symbol}/subsidiaries", response_model=ApiResponse, summary="Công ty con")
async def company_subsidiaries(symbol: str):
    """Lấy danh sách công ty con."""
    try:
        data = vs.get_company_subsidiaries(symbol)
        return ApiResponse(data=data, count=len(data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/company/{symbol}/ownership", response_model=ApiResponse, summary="Cơ cấu sở hữu")
async def company_ownership(symbol: str):
    """Lấy cơ cấu sở hữu."""
    try:
        data = vs.get_company_ownership(symbol)
        return ApiResponse(data=data, count=len(data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/company/{symbol}/insider-trading", response_model=ApiResponse, summary="Giao dịch nội bộ")
async def company_insider_trading(symbol: str):
    """Lấy lịch sử giao dịch nội bộ."""
    try:
        data = vs.get_company_insider_trading(symbol)
        return ApiResponse(data=data, count=len(data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/company/{symbol}/capital-history", response_model=ApiResponse, summary="Lịch sử thay đổi vốn")
async def company_capital_history(symbol: str):
    """Lấy lịch sử thay đổi vốn."""
    try:
        data = vs.get_company_capital_history(symbol)
        return ApiResponse(data=data, count=len(data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/company/{symbol}/news", response_model=ApiResponse, summary="Tin tức công ty")
async def company_news(symbol: str):
    """Lấy tin tức liên quan đến công ty."""
    try:
        data = vs.get_company_news(symbol)
        return ApiResponse(data=data, count=len(data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/company/{symbol}/events", response_model=ApiResponse, summary="Sự kiện doanh nghiệp")
async def company_events(symbol: str):
    """Lấy các sự kiện doanh nghiệp sắp tới."""
    try:
        data = vs.get_company_events(symbol)
        return ApiResponse(data=data, count=len(data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Index ───────────────────────────────────────────────────

@router.get("/index/list", response_model=ApiResponse, summary="Danh sách chỉ số")
async def index_list():
    """Lấy danh sách tất cả chỉ số thị trường."""
    try:
        data = vs.get_index_list()
        return ApiResponse(data=data, count=len(data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/index/groups", response_model=ApiResponse, summary="Nhóm chỉ số")
async def index_groups():
    """Lấy danh sách nhóm chỉ số hỗ trợ."""
    try:
        data = vs.get_index_groups()
        return ApiResponse(data=data, count=len(data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/index/info", response_model=ApiResponse, summary="Thông tin chỉ số")
async def index_info():
    """Lấy metadata tất cả chỉ số thị trường."""
    try:
        data = vs.get_index_info()
        return ApiResponse(data=data, count=len(data) if isinstance(data, list) else 1)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/index/{index}/members", response_model=ApiResponse, summary="Thành phần chỉ số")
async def index_members(index: str):
    """Lấy danh sách mã cổ phiếu thành phần của chỉ số."""
    try:
        data = vs.get_index_members(index)
        return ApiResponse(data=data, count=len(data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Industry ────────────────────────────────────────────────

@router.get("/industry/list", response_model=ApiResponse, summary="Phân ngành ICB")
async def industry_list():
    """Lấy danh sách phân ngành ICB."""
    try:
        data = vs.get_industry_list()
        return ApiResponse(data=data, count=len(data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/industry/sectors", response_model=ApiResponse, summary="Mã theo ngành")
async def industry_sectors():
    """Lấy danh sách mã cổ phiếu phân theo ngành."""
    try:
        data = vs.get_industry_sectors()
        return ApiResponse(data=data, count=len(data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Search ──────────────────────────────────────────────────

@router.get("/search", response_model=ApiResponse, summary="Tìm kiếm mã chứng khoán")
async def search(query: str = Query(..., min_length=1, description="Từ khóa tìm kiếm (mã CK hoặc tên)")):
    """Tìm kiếm mã chứng khoán toàn cầu."""
    try:
        data = vs.search_symbol(query)
        return ApiResponse(data=data, count=len(data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search/info", response_model=ApiResponse, summary="Tìm kiếm thông tin chi tiết")
async def search_info(query: str = Query(..., min_length=1, description="Từ khóa tìm kiếm")):
    """Tìm kiếm thông tin chi tiết tài sản."""
    try:
        data = vs.search_info(query)
        return ApiResponse(data=data, count=len(data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Market Status ───────────────────────────────────────────

@router.get("/market/status", response_model=ApiResponse, summary="Trạng thái thị trường")
async def market_status():
    """Lấy trạng thái thị trường hiện tại."""
    try:
        data = vs.get_market_status()
        return ApiResponse(data=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
