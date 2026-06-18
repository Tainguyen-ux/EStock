# 📊 EStock API Documentation

## Tổng quan

**Base URL**: `http://localhost:8000`

**Response Format**: Tất cả endpoint trả về cùng cấu trúc:

```json
{
  "success": true,
  "data": [...],
  "message": "",
  "timestamp": "2026-06-17T13:00:00",
  "count": 90 
}
```

---

## 🔧 System Endpoints

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/` | Thông tin API |
| GET | `/health` | Health check + cache stats |
| POST | `/cache/clear` | Xóa toàn bộ cache |

---

## 📈 1. Market Data — Dữ liệu Thị trường

### 1.1 Bảng giá toàn thị trường
```
GET /api/market/quote
```
| Param | Type | Default | Mô tả |
|-------|------|---------|-------|
| symbols | query | "" | Danh sách mã chứng khoán (FPT,TCB,...). Để trống để lấy rổ VN30. |

### 1.2 OHLCV cổ phiếu
```
GET /api/market/equity/{symbol}/ohlcv
```
| Param | Type | Default | Mô tả |
|-------|------|---------|-------|
| symbol | path | required | Mã CK (VCB, FPT, ...) |
| start | query | "" | Ngày bắt đầu (YYYY-MM-DD) |
| end | query | "" | Ngày kết thúc (YYYY-MM-DD) |
| interval | query | "1D" | 1m, 5m, 15m, 30m, 1H, 1D, 1W, 1M |
| length | query | 90 | Số nến (dùng khi không có start/end) |

**Ví dụ:**
```
GET /api/market/equity/VCB/ohlcv?start=2024-01-01&end=2024-12-31&interval=1D
GET /api/market/equity/FPT/ohlcv?length=90&interval=1D
```

### 1.3 Quote real-time cổ phiếu
```
GET /api/market/equity/{symbol}/quote
```

### 1.4 Dữ liệu khớp lệnh tick-by-tick
```
GET /api/market/equity/{symbol}/trades
```

### 1.5 OHLCV chỉ số thị trường
```
GET /api/market/index/{index}/ohlcv
```
**Ví dụ:** `GET /api/market/index/VNINDEX/ohlcv?length=60`

### 1.6 OHLCV ngoại hối
```
GET /api/market/forex/{pair}/ohlcv
```
**Ví dụ:** `GET /api/market/forex/USDVND/ohlcv?length=30`

### 1.7 OHLCV crypto
```
GET /api/market/crypto/{pair}/ohlcv
```
**Ví dụ:** `GET /api/market/crypto/BTCUSD/ohlcv?length=60`

### 1.8 OHLCV hàng hóa
```
GET /api/market/commodity/{symbol}/ohlcv
```

---

## 📋 2. Reference Data — Dữ liệu Tham chiếu

### 2.1 Danh sách cổ phiếu

| Endpoint | Mô tả |
|----------|-------|
| `GET /api/reference/equity/list` | Tất cả mã niêm yết |
| `GET /api/reference/equity/by-group?group=VN30` | Theo nhóm |
| `GET /api/reference/equity/by-industry` | Theo ngành |
| `GET /api/reference/equity/by-exchange?exchange=HOSE` | Theo sàn |

### 2.2 Thông tin công ty

| Endpoint | Mô tả |
|----------|-------|
| `GET /api/reference/company/{symbol}/info` | Tổng quan DN |
| `GET /api/reference/company/{symbol}/shareholders` | Cổ đông lớn |
| `GET /api/reference/company/{symbol}/officers` | Ban lãnh đạo |
| `GET /api/reference/company/{symbol}/subsidiaries` | Công ty con |
| `GET /api/reference/company/{symbol}/ownership` | Cơ cấu sở hữu |
| `GET /api/reference/company/{symbol}/insider-trading` | GD nội bộ |
| `GET /api/reference/company/{symbol}/capital-history` | Lịch sử vốn |
| `GET /api/reference/company/{symbol}/news` | Tin tức |
| `GET /api/reference/company/{symbol}/events` | Sự kiện |

**Ví dụ:** `GET /api/reference/company/FPT/info`

### 2.3 Chỉ số thị trường

| Endpoint | Mô tả |
|----------|-------|
| `GET /api/reference/index/list` | DS chỉ số |
| `GET /api/reference/index/groups` | Nhóm chỉ số |
| `GET /api/reference/index/info` | Metadata chỉ số |
| `GET /api/reference/index/{index}/members` | Thành phần |

### 2.4 Ngành

| Endpoint | Mô tả |
|----------|-------|
| `GET /api/reference/industry/list` | Phân ngành ICB |
| `GET /api/reference/industry/sectors` | Mã theo ngành |

### 2.5 Tìm kiếm

| Endpoint | Mô tả |
|----------|-------|
| `GET /api/reference/search?query=FPT` | Tìm mã CK |
| `GET /api/reference/search/info?query=vietcombank` | Tìm chi tiết |

### 2.6 Trạng thái thị trường
```
GET /api/reference/market/status
```

---

## 💰 3. Fundamental Data — Báo cáo Tài chính

| Endpoint | Mô tả |
|----------|-------|
| `GET /api/fundamental/{symbol}/balance-sheet` | Bảng CĐKT |
| `GET /api/fundamental/{symbol}/income-statement` | KQHĐKD |
| `GET /api/fundamental/{symbol}/cash-flow` | LCTT |
| `GET /api/fundamental/{symbol}/ratios` | Chỉ số tài chính |

**Query params chung:**

| Param | Type | Default | Mô tả |
|-------|------|---------|-------|
| period | query | "year" | "year" hoặc "quarter" |

**Ví dụ:**
```
GET /api/fundamental/VCB/balance-sheet?period=quarter
GET /api/fundamental/FPT/ratios?period=year
```

---

## 🔍 4. Stock Screener — Bộ lọc Cổ phiếu

### 4.1 Lọc theo Phân tích Cơ bản (FA)
```
POST /api/screener/fundamental
```

**Request body:**
```json
{
  "exchange": "",
  "group": "VN30",
  "pe_max": 15,
  "roe_min": 15,
  "debt_equity_max": 1.5,
  "limit": 50
}
```

| Field | Type | Mô tả |
|-------|------|-------|
| exchange | string | Sàn: HOSE, HNX, UPCOM |
| group | string | Nhóm: VN30, HNX30, ... |
| pe_max / pe_min | float | Khoảng P/E |
| pb_max / pb_min | float | Khoảng P/B |
| roe_min | float | ROE tối thiểu (%) |
| roa_min | float | ROA tối thiểu (%) |
| debt_equity_max | float | Nợ/VCSH tối đa |
| gross_margin_min | float | Biên LN gộp tối thiểu (%) |
| net_margin_min | float | Biên LN ròng tối thiểu (%) |
| revenue_growth_min | float | Tăng trưởng DT tối thiểu (%) |
| profit_growth_min | float | Tăng trưởng LN tối thiểu (%) |
| limit | int | Số kết quả tối đa |

### 4.2 Lọc theo Phân tích Kỹ thuật (TA)
```
POST /api/screener/technical
```

**Request body:**
```json
{
  "group": "VN30",
  "rsi_oversold": true,
  "volume_spike": true,
  "volume_spike_ratio": 2.0,
  "lookback_days": 60,
  "limit": 20
}
```

| Field | Type | Mô tả |
|-------|------|-------|
| symbols | list | Danh sách mã cụ thể |
| ma_cross_up | bool | Giá cắt lên MA20 |
| ma_cross_down | bool | Giá cắt xuống MA20 |
| above_ma20 | bool | Giá trên MA20 |
| above_ma50 | bool | Giá trên MA50 |
| rsi_oversold | bool | RSI < 30 |
| rsi_overbought | bool | RSI > 70 |
| rsi_min / rsi_max | float | Khoảng RSI |
| volume_spike | bool | KL đột biến |
| volume_spike_ratio | float | Hệ số đột biến KL (mặc định 2.0x) |
| macd_cross_up | bool | MACD cắt lên signal |
| lookback_days | int | Số phiên tính toán |

### 4.3 So sánh nhiều mã
```
POST /api/screener/compare
```

**Request body:**
```json
{
  "symbols": ["VCB", "TCB", "BID", "MBB"],
  "include_price": true,
  "include_fundamental": true,
  "period": "90"
}
```

---

## 🌍 5. Macro Data — Dữ liệu Vĩ mô

| Endpoint | Mô tả |
|----------|-------|
| `GET /api/macro/gold?source=sjc` | Giá vàng (sjc/doji/pnj) |
| `GET /api/macro/exchange-rate` | Tỷ giá VCB |
| `GET /api/macro/forex/{pair}/ohlcv` | Lịch sử FX (USDVND) |

---

## 📊 6. Derivatives — Phái sinh

### Futures
| Endpoint | Mô tả |
|----------|-------|
| `GET /api/derivatives/futures/list` | DS hợp đồng |
| `GET /api/derivatives/futures/info` | Thông số kỹ thuật |
| `GET /api/derivatives/futures/{symbol}/ohlcv` | OHLCV |
| `GET /api/derivatives/futures/{symbol}/quote` | Quote |
| `GET /api/derivatives/futures/{symbol}/trades` | Trades |

### Warrants
| Endpoint | Mô tả |
|----------|-------|
| `GET /api/derivatives/warrants/list` | DS chứng quyền |
| `GET /api/derivatives/warrants/info` | Thông số |
| `GET /api/derivatives/warrants/{symbol}/ohlcv` | OHLCV |
| `GET /api/derivatives/warrants/{symbol}/quote` | Quote |

### ETF
| Endpoint | Mô tả |
|----------|-------|
| `GET /api/derivatives/etf/list` | DS ETF |
| `GET /api/derivatives/etf/{symbol}/ohlcv` | OHLCV |
| `GET /api/derivatives/etf/{symbol}/quote` | Quote |

---

## 🏦 7. Investment Funds — Quỹ đầu tư

| Endpoint | Mô tả |
|----------|-------|
| `GET /api/funds/list` | DS quỹ mở |
| `GET /api/funds/{fund_code}/nav` | Lịch sử NAV |
| `GET /api/funds/{fund_code}/top-holding` | Top nắm giữ |
| `GET /api/funds/{fund_code}/industry-holding` | Phân bổ ngành |
| `GET /api/funds/{fund_code}/asset-holding` | Phân bổ tài sản |

---

## 📉 8. Technical Analysis — Phân tích Kỹ thuật

### 8.1 Tất cả chỉ báo
```
GET /api/technical/{symbol}/indicators
```
| Param | Default | Mô tả |
|-------|---------|-------|
| length | 200 | Số phiên lịch sử |
| sma_periods | "5,10,20,50,200" | Chu kỳ SMA |
| ema_periods | "12,26" | Chu kỳ EMA |
| rsi_period | 14 | Chu kỳ RSI |

**Response bao gồm**: SMA, EMA, RSI, MACD, Bollinger Bands, Stochastic, ATR, Volume ratio

### 8.2 Chỉ báo riêng lẻ

| Endpoint | Params | Mô tả |
|----------|--------|-------|
| `GET /api/technical/{symbol}/sma` | period=20 | Simple Moving Average |
| `GET /api/technical/{symbol}/ema` | period=20 | Exponential Moving Average |
| `GET /api/technical/{symbol}/rsi` | period=14 | Relative Strength Index |
| `GET /api/technical/{symbol}/macd` | fast=12, slow=26, signal=9 | MACD |
| `GET /api/technical/{symbol}/bollinger` | period=20, std_dev=2.0 | Bollinger Bands |
| `GET /api/technical/{symbol}/stochastic` | k_period=14, d_period=3 | Stochastic Oscillator |
| `GET /api/technical/{symbol}/atr` | period=14 | Average True Range |

**Ví dụ:**
```
GET /api/technical/VCB/rsi?period=14&length=100
GET /api/technical/FPT/macd?fast=12&slow=26&signal=9&length=200
GET /api/technical/TCB/indicators?sma_periods=5,20,50&length=300
```

---

## 🔐 Xác thực & Rate Limit

| Tier | Rate Limit | BCTC | Yêu cầu |
|------|-----------|------|---------|
| Guest | 20 req/min | 4 kỳ | Không cần đăng ký |
| Community | 60 req/min | 8 kỳ | Đăng ký miễn phí |
| Sponsor | 180+ req/min | Đầy đủ | Tài trợ dự án |

Cấu hình API key trong file `.env`:
```
VNSTOCK_API_KEY=vnstock_YOUR_KEY_HERE
```

---

## ⚠️ Error Handling

Khi lỗi xảy ra, API trả về:
```json
{
  "detail": "Error message from vnstock"
}
```

HTTP Status codes:
- `200` — Thành công
- `422` — Validation error (sai params)
- `500` — Lỗi server / vnstock API

---

## 🚀 Deployment

### Development
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker (tùy chọn)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 📊 Tổng kết Endpoints

| Nhóm | Số Endpoints | Prefix |
|------|-------------|--------|
| System | 3 | `/` |
| Market Data | 8 | `/api/market` |
| Reference Data | 20 | `/api/reference` |
| Fundamental | 4 | `/api/fundamental` |
| Screener | 3 | `/api/screener` |
| Macro | 3 | `/api/macro` |
| Derivatives | 12 | `/api/derivatives` |
| Funds | 5 | `/api/funds` |
| Technical | 8 | `/api/technical` |
| **Tổng** | **66** | |
