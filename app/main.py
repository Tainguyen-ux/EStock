"""
EStock API — Vietnamese Stock Market Data Service.
Powered by vnstock 4.0+ Unified UI.

FastAPI application entry point with CORS, lifespan, and all routers.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.config import get_settings
from app.dependencies import init_vnstock
from app.utils.cache import clear_cache, cache_stats
from app.schemas.common import ApiResponse

# Import routers
from app.routers import (
    market,
    reference,
    fundamental,
    screener,
    macro,
    derivatives,
    funds,
    technical,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: startup and shutdown events."""
    # Startup
    logger.info("=" * 60)
    logger.info("EStock API starting up...")
    logger.info("Initializing vnstock 4.0+ (Unified UI)...")
    try:
        init_vnstock()
        logger.info("vnstock initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize vnstock: {e}")
        logger.warning("API will attempt lazy initialization on first request")
    logger.info("=" * 60)

    yield

    # Shutdown
    logger.info("EStock API shutting down...")
    clear_cache()
    logger.info("Cache cleared. Goodbye!")


# ── Create FastAPI App ──────────────────────────────────────
settings = get_settings()

app = FastAPI(
    title="EStock API",
    description="""
## 📊 Vietnamese Stock Market Data API

Hệ thống API dữ liệu chứng khoán Việt Nam toàn diện, powered by **vnstock 4.0+**.

### Nhóm chức năng:
- **Market Data**: Giá OHLCV, quote real-time, dữ liệu khớp lệnh
- **Reference Data**: Danh sách niêm yết, thông tin công ty, chỉ số, ngành
- **Fundamental Data**: Báo cáo tài chính, chỉ số tài chính
- **Stock Screener**: Bộ lọc FA (cơ bản) + TA (kỹ thuật)
- **Macro Data**: Giá vàng, tỷ giá ngoại tệ
- **Derivatives**: Hợp đồng tương lai, chứng quyền, ETF
- **Investment Funds**: Quỹ mở, NAV, phân bổ danh mục
- **Technical Analysis**: SMA, EMA, RSI, MACD, Bollinger Bands, Stochastic, ATR

### Lưu ý:
- Dữ liệu real-time chỉ khả dụng trong giờ giao dịch (9:00-15:00 GMT+7)
- Rate limit tùy theo cấp tài khoản vnstock (Guest: 20 req/min)
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# ── CORS Middleware ─────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Register Routers ───────────────────────────────────────
app.include_router(market.router)
app.include_router(reference.router)
app.include_router(fundamental.router)
app.include_router(screener.router)
app.include_router(macro.router)
app.include_router(derivatives.router)
app.include_router(funds.router)
app.include_router(technical.router)


# ── Root & Health Endpoints ────────────────────────────────

@app.get("/", response_model=ApiResponse, tags=["System"])
async def root():
    """API root — thông tin cơ bản."""
    return ApiResponse(
        data={
            "name": "EStock API",
            "version": "1.0.0",
            "engine": "vnstock 4.0+ (Unified UI)",
            "docs": "/docs",
            "redoc": "/redoc",
        },
        message="EStock API is running"
    )


@app.get("/health", response_model=ApiResponse, tags=["System"])
async def health_check():
    """Health check endpoint."""
    return ApiResponse(
        data={"status": "healthy", "cache": cache_stats()},
        message="OK"
    )


@app.post("/cache/clear", response_model=ApiResponse, tags=["System"])
async def clear_all_cache():
    """Xóa toàn bộ cache."""
    clear_cache()
    return ApiResponse(message="Cache cleared successfully")


# ── Run directly ────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
