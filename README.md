# EStock API — Vietnamese Stock Market Data Service

> 📊 Hệ thống API dữ liệu chứng khoán Việt Nam toàn diện, powered by **vnstock 4.0+**

## Quick Start

```bash
# 1. Cài đặt dependencies
pip install -r requirements.txt

# 2. (Tùy chọn) Cấu hình API key
cp .env.example .env
# Sửa file .env, thêm VNSTOCK_API_KEY nếu có

# 3. Chạy server
uvicorn app.main:app --reload --port 8000

# 4. Mở Swagger UI
# http://localhost:8000/docs
```

## Kiến trúc

```
app/
├── main.py              # FastAPI entry point
├── config.py            # Settings (.env)
├── dependencies.py      # Vnstock singleton instances
├── routers/             # 8 API router groups
│   ├── market.py        # Giá OHLCV, quote, trades
│   ├── reference.py     # Listing, company, index, search
│   ├── fundamental.py   # BCTC, chỉ số tài chính
│   ├── screener.py      # Bộ lọc FA + TA
│   ├── macro.py         # Vàng, tỷ giá
│   ├── derivatives.py   # Futures, warrants, ETF
│   ├── funds.py         # Quỹ mở
│   └── technical.py     # Chỉ báo kỹ thuật
├── services/            # Business logic
│   ├── vnstock_service.py
│   ├── technical_service.py
│   └── screener_service.py
├── schemas/             # Pydantic models
└── utils/               # Cache utilities
```

## Công nghệ

| Thành phần | Công nghệ |
|---|---|
| Framework | FastAPI |
| Data Engine | vnstock 4.0+ (Unified UI) |
| Validation | Pydantic v2 |
| Caching | cachetools (TTL in-memory) |
| Documentation | Auto-generated Swagger + ReDoc |

## Tài liệu API

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Chi tiết**: Xem file `API_DOCUMENTATION.md`
