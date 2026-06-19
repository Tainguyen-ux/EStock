# 📊 EStock API Documentation

> **Phiên bản**: 1.0.0 · **Cập nhật lần cuối**: 2026-06-19
>
> Tài liệu này được sắp xếp theo **thứ tự tích hợp** — các API trả về danh sách (list) luôn nằm **trước** các API cần truyền tham số lấy từ danh sách đó.

## Tổng quan

**Base URL**: `http://34.87.142.4:8000`

**Định dạng phản hồi chung (Response Wrapper)**:

```json
{
  "success": true,
  "data": [],
  "message": "Thông tin bổ sung",
  "timestamp": "2026-06-19T09:30:00.123456",
  "count": 0
}
```

| Trường | Kiểu | Mô tả |
|--------|------|-------|
| `success` | boolean | `true` nếu thành công, `false` nếu lỗi |
| `data` | array \| object | Dữ liệu kết quả |
| `message` | string | Thông báo bổ sung hoặc lỗi |
| `timestamp` | string | Thời gian thực thi (ISO-8601) |
| `count` | integer \| null | Số lượng bản ghi trong `data` |

**Quy ước tham số OHLCV chung** (áp dụng cho tất cả endpoint OHLCV):

| Param | Type | Default | Mô tả |
|-------|------|---------|-------|
| start | query | "" | Ngày bắt đầu `YYYY-MM-DD` |
| end | query | "" | Ngày kết thúc `YYYY-MM-DD` |
| interval | query | "1D" | Khung thời gian: `1m`, `5m`, `15m`, `30m`, `1H`, `1D`, `1W`, `1M` |
| length | query | 90 | Số nến lịch sử (dùng khi không truyền `start`/`end`) |

---

## 🔧 0. System — Hệ thống

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/` | Thông tin phiên bản hệ thống |
| GET | `/health` | Health check & thống kê cache |
| POST | `/cache/clear` | Xóa toàn bộ cache |

---

## 📋 1. Reference Data — Dữ liệu Tham chiếu

> ⚡ **Gọi đầu tiên khi tích hợp.** Nhóm này cung cấp danh sách mã chứng khoán (`symbol`), mã chỉ số (`index`), mã ngành, v.v. — là tham số bắt buộc cho hầu hết các API còn lại.

### 1.1 Danh sách mã cổ phiếu niêm yết

Trả về danh sách `symbol` để dùng cho các API Market Data, Fundamental, Technical.

| # | Endpoint | Mô tả | Param đáng chú ý |
|---|----------|-------|-------------------|
| 1 | `GET /api/reference/equity/list` | Tất cả mã niêm yết | — |
| 2 | `GET /api/reference/equity/by-group` | Lọc theo nhóm chỉ số | `group` (default: `VN30`) |
| 3 | `GET /api/reference/equity/by-exchange` | Lọc theo sàn giao dịch | `exchange` (`HOSE`, `HNX`, `UPCOM`) |
| 4 | `GET /api/reference/equity/by-industry` | Phân nhóm theo ngành ICB | — |

→ **Output**: Mảng chứa trường `symbol` (ví dụ: `FPT`, `TCB`, `VCB`) dùng làm `{symbol}` cho các API phía sau.

### 1.2 Chỉ số thị trường (Index)

Trả về danh sách mã `index` để dùng cho API OHLCV chỉ số & thành phần rổ.

| # | Endpoint | Mô tả |
|---|----------|-------|
| 1 | `GET /api/reference/index/list` | Danh sách tất cả chỉ số |
| 2 | `GET /api/reference/index/groups` | Danh sách nhóm chỉ số hỗ trợ |
| 3 | `GET /api/reference/index/info` | Metadata kỹ thuật các chỉ số |
| 4 | `GET /api/reference/index/{index}/members` | Mã thành phần của chỉ số _(lấy `{index}` từ endpoint 1)_ |

→ **Output endpoint 1**: Trả về các giá trị `index` như `VNINDEX`, `HNX30`, `VN30`.

### 1.3 Ngành (Industry)

| # | Endpoint | Mô tả |
|---|----------|-------|
| 1 | `GET /api/reference/industry/list` | Cây phân ngành ICB |
| 2 | `GET /api/reference/industry/sectors` | Mã cổ phiếu phân theo ngành |

### 1.4 Thông tin doanh nghiệp

> Yêu cầu `{symbol}` từ mục 1.1.

| # | Endpoint | Mô tả |
|---|----------|-------|
| 1 | `GET /api/reference/company/{symbol}/info` | Thông tin cơ bản doanh nghiệp |
| 2 | `GET /api/reference/company/{symbol}/shareholders` | Cổ đông lớn |
| 3 | `GET /api/reference/company/{symbol}/officers` | Ban lãnh đạo |
| 4 | `GET /api/reference/company/{symbol}/subsidiaries` | Công ty con |
| 5 | `GET /api/reference/company/{symbol}/ownership` | Cơ cấu sở hữu |
| 6 | `GET /api/reference/company/{symbol}/insider-trading` | Giao dịch nội bộ |
| 7 | `GET /api/reference/company/{symbol}/capital-history` | Lịch sử thay đổi vốn |
| 8 | `GET /api/reference/company/{symbol}/news` | Tin tức liên quan |
| 9 | `GET /api/reference/company/{symbol}/events` | Sự kiện (cổ tức, ĐHĐCĐ) |

**Ví dụ response `news`**:
```json
[
  {
    "title": "Theo dấu dòng tiền cá mập...",
    "head": "Khối ngoại bán ròng gần 1.9 ngàn tỷ...",
    "publish_time": "2026-06-18 19:02:00",
    "url": "https://vietstock.vn/2026/06/...",
    "article_id": 1455969
  }
]
```

### 1.5 Tìm kiếm & Trạng thái

| # | Endpoint | Mô tả | Param |
|---|----------|-------|-------|
| 1 | `GET /api/reference/search` | Tìm mã chứng khoán | `query` (required) |
| 2 | `GET /api/reference/search/info` | Tìm thông tin chi tiết tài sản | `query` (required) |
| 3 | `GET /api/reference/market/status` | Trạng thái phiên giao dịch | — |

---

## 📈 2. Market Data — Dữ liệu Thị trường

> Yêu cầu `{symbol}` từ mục 1.1, `{index}` từ mục 1.2.

### 2.1 Bảng giá toàn thị trường
```http
GET /api/market/quote
```
| Param | Type | Default | Mô tả |
|-------|------|---------|-------|
| symbols | query | "" | Mã CK phân cách bằng dấu phẩy (`FPT,TCB,VCB`). Để trống = rổ VN30. |

**Ví dụ response**:
```json
[
  {
    "symbol": "FPT",
    "exchange": "HOSE",
    "ceiling_price": 77300,
    "floor_price": 67300,
    "reference_price": 72300,
    "open_price": 72300,
    "high_price": 72300,
    "low_price": 71500,
    "close_price": 71600,
    "volume_accumulated": 13665800,
    "price_change": -700,
    "percent_change": -0.968,
    "bid_price_1": 71600,
    "ask_price_1": 71700,
    "foreign_buy_volume": 836613,
    "foreign_sell_volume": 7822974
  }
]
```

### 2.2 Cổ phiếu (Equity)

| # | Endpoint | Mô tả |
|---|----------|-------|
| 1 | `GET /api/market/equity/{symbol}/ohlcv` | OHLCV lịch sử _(params OHLCV chung)_ |
| 2 | `GET /api/market/equity/{symbol}/quote` | Quote real-time |
| 3 | `GET /api/market/equity/{symbol}/trades` | Khớp lệnh tick-by-tick |

**Ví dụ OHLCV**:
```json
[{ "time": "2026-06-17 07:00:00", "open": 73.3, "high": 73.4, "low": 72.2, "close": 72.3, "volume": 10652200 }]
```

### 2.3 Chỉ số, Ngoại hối, Crypto, Hàng hóa

| # | Endpoint | Path Param | Ví dụ |
|---|----------|------------|-------|
| 1 | `GET /api/market/index/{index}/ohlcv` | `{index}` từ mục 1.2 | `VNINDEX`, `HNX30` |
| 2 | `GET /api/market/forex/{pair}/ohlcv` | Cặp ngoại tệ | `USDVND`, `EURVND` |
| 3 | `GET /api/market/crypto/{pair}/ohlcv` | Cặp crypto | `BTCUSD`, `ETHUSD` |
| 4 | `GET /api/market/commodity/{symbol}/ohlcv` | Ký hiệu hàng hóa | `XAUUSD`, `WTI` |

> Tất cả sử dụng **params OHLCV chung** ở phần Tổng quan.

---

## 💰 3. Fundamental Data — Báo cáo Tài chính

> Yêu cầu `{symbol}` từ mục 1.1.

### 3.1 Báo cáo tài chính

| # | Endpoint | Mô tả |
|---|----------|-------|
| 1 | `GET /api/fundamental/{symbol}/balance-sheet` | Bảng cân đối kế toán |
| 2 | `GET /api/fundamental/{symbol}/income-statement` | Kết quả HĐKD |
| 3 | `GET /api/fundamental/{symbol}/cash-flow` | Lưu chuyển tiền tệ |
| 4 | `GET /api/fundamental/{symbol}/ratios` | Chỉ số tài chính (P/E, P/B, ROE, ROA, EPS) |

| Param | Type | Default | Mô tả |
|-------|------|---------|-------|
| period | query | "year" | `year` (theo năm) hoặc `quarter` (theo quý) |

**Ví dụ response**:
```json
[
  {
    "item": "Tài sản ngắn hạn",
    "item_id": "short_term_assets",
    "2025": 28450122000000,
    "2024": 26110900000000
  }
]
```

---

## 🔐 4. Derivatives — Phái sinh & ETF

### 4.1 Hợp đồng Tương lai (Futures)

| # | Endpoint | Mô tả | Ghi chú |
|---|----------|-------|---------|
| 1 | `GET /api/derivatives/futures/list` | **Danh sách mã futures** | → Lấy `{symbol}` |
| 2 | `GET /api/derivatives/futures/info` | Thông số kỹ thuật | — |
| 3 | `GET /api/derivatives/futures/{symbol}/ohlcv` | OHLCV lịch sử | Cần `{symbol}` từ #1 |
| 4 | `GET /api/derivatives/futures/{symbol}/quote` | Giá real-time | Cần `{symbol}` từ #1 |
| 5 | `GET /api/derivatives/futures/{symbol}/trades` | Khớp lệnh tick-by-tick | Cần `{symbol}` từ #1 |

### 4.2 Chứng quyền (Covered Warrants)

| # | Endpoint | Mô tả | Ghi chú |
|---|----------|-------|---------|
| 1 | `GET /api/derivatives/warrants/list` | **Danh sách mã CW** | → Lấy `{symbol}` |
| 2 | `GET /api/derivatives/warrants/info` | Thông số kỹ thuật | — |
| 3 | `GET /api/derivatives/warrants/{symbol}/ohlcv` | OHLCV lịch sử | Cần `{symbol}` từ #1 |
| 4 | `GET /api/derivatives/warrants/{symbol}/quote` | Giá real-time | Cần `{symbol}` từ #1 |

### 4.3 Quỹ ETF

| # | Endpoint | Mô tả | Ghi chú |
|---|----------|-------|---------|
| 1 | `GET /api/derivatives/etf/list` | **Danh sách ETF** | → Lấy `{symbol}` |
| 2 | `GET /api/derivatives/etf/{symbol}/ohlcv` | OHLCV lịch sử | Cần `{symbol}` từ #1 |
| 3 | `GET /api/derivatives/etf/{symbol}/quote` | Giá real-time | Cần `{symbol}` từ #1 |

---

## 🏦 5. Investment Funds — Quỹ đầu tư mở

| # | Endpoint | Mô tả | Ghi chú |
|---|----------|-------|---------|
| 1 | `GET /api/funds/list` | **Danh sách quỹ mở** | → Lấy `{fund_code}` |
| 2 | `GET /api/funds/{fund_code}/nav` | Lịch sử NAV | Cần `{fund_code}` từ #1 |
| 3 | `GET /api/funds/{fund_code}/top-holding` | Top cổ phiếu nắm giữ | Cần `{fund_code}` từ #1 |
| 4 | `GET /api/funds/{fund_code}/industry-holding` | Phân bổ theo ngành | Cần `{fund_code}` từ #1 |
| 5 | `GET /api/funds/{fund_code}/asset-holding` | Phân bổ theo loại tài sản | Cần `{fund_code}` từ #1 |

---

## 🌍 6. Macro Data — Dữ liệu Vĩ mô

> Không yêu cầu tham số từ API khác.

### 6.1 Giá vàng trong nước
```http
GET /api/macro/gold
```
| Param | Type | Default | Mô tả |
|-------|------|---------|-------|
| source | query | "sjc" | Nguồn: `sjc`, `doji`, `pnj` |

### 6.2 Tỷ giá ngoại tệ
```http
GET /api/macro/exchange-rate
```
Trả về bảng tỷ giá mua/bán Vietcombank.

### 6.3 Lịch sử tỷ giá ngoại hối
```http
GET /api/macro/forex/{pair}/ohlcv
```
`{pair}` là cặp ngoại tệ (ví dụ: `USDVND`, `EURVND`). Params OHLCV chung.

---

## 📉 7. Technical Analysis — Phân tích Kỹ thuật

> Yêu cầu `{symbol}` từ mục 1.1. Dữ liệu OHLCV được tự động lấy từ API Market Data.

### 7.1 Tất cả chỉ báo tổng hợp
```http
GET /api/technical/{symbol}/indicators
```
| Param | Type | Default | Mô tả |
|-------|------|---------|-------|
| length | query | 200 | Số phiên lịch sử |
| sma_periods | query | "5,10,20,50,200" | Chu kỳ SMA (phân cách bằng dấu phẩy) |
| ema_periods | query | "12,26" | Chu kỳ EMA |
| rsi_period | query | 14 | Chu kỳ RSI |

### 7.2 Chỉ báo riêng lẻ

| # | Endpoint | Chỉ báo | Params riêng |
|---|----------|---------|-------------|
| 1 | `GET /api/technical/{symbol}/sma` | Simple Moving Average | `period`=20, `length`=100 |
| 2 | `GET /api/technical/{symbol}/ema` | Exponential Moving Average | `period`=20, `length`=100 |
| 3 | `GET /api/technical/{symbol}/rsi` | Relative Strength Index | `period`=14, `length`=100 |
| 4 | `GET /api/technical/{symbol}/macd` | MACD | `fast`=12, `slow`=26, `signal`=9, `length`=100 |
| 5 | `GET /api/technical/{symbol}/bollinger` | Bollinger Bands | `period`=20, `std_dev`=2.0, `length`=100 |
| 6 | `GET /api/technical/{symbol}/stochastic` | Stochastic Oscillator | `k_period`=14, `d_period`=3, `length`=100 |
| 7 | `GET /api/technical/{symbol}/atr` | Average True Range | `period`=14, `length`=100 |

---

## 🔍 8. Stock Screener — Bộ lọc Cổ phiếu

> Screener tự động lấy danh sách mã từ Reference Data dựa trên `exchange`/`group` truyền vào.

### 8.1 Lọc theo Phân tích Cơ bản (FA)
```http
POST /api/screener/fundamental
```
**Request Body:**

| Param | Type | Mô tả |
|-------|------|-------|
| exchange | string? | Sàn giao dịch |
| group | string? | Nhóm chỉ số (VN30, HNX30...) |
| pe_min / pe_max | float? | Khoảng P/E |
| pb_min / pb_max | float? | Khoảng P/B |
| roe_min / roa_min | float? | ROE / ROA tối thiểu (%) |
| gross_margin_min / net_margin_min | float? | Biên lợi nhuận tối thiểu (%) |
| debt_equity_max | float? | Nợ/Vốn CSH tối đa |
| revenue_growth_min / profit_growth_min | float? | Tăng trưởng tối thiểu (%) |

### 8.2 Lọc theo Phân tích Kỹ thuật (TA)
```http
POST /api/screener/technical
```
**Request Body:**

| Param | Type | Mô tả |
|-------|------|-------|
| symbols | string[]? | Mã CK cụ thể (nếu không dùng group/exchange) |
| group | string? | Nhóm chỉ số |
| lookback_days | integer | Số phiên đánh giá tín hiệu |
| ma_cross_up / ma_cross_down | boolean? | MA20 cắt lên/xuống MA50 |
| above_ma20 / above_ma50 | boolean? | Giá trên MA20/MA50 |
| rsi_oversold / rsi_overbought | boolean? | RSI <30 / >70 |
| volume_spike | boolean? | Đột biến khối lượng |
| volume_spike_ratio | float? | Tỷ số đột biến (default: 2.0) |
| macd_cross_up | boolean? | MACD cắt lên Signal |

### 8.3 So sánh nhiều mã
```http
POST /api/screener/compare
```
**Request Body:**

| Param | Type | Mô tả |
|-------|------|-------|
| symbols | string[] | Danh sách mã so sánh (`["FPT","TCB","VCB"]`) |
| include_price | boolean | Bao gồm giá đóng cửa |
| include_fundamental | boolean | Bao gồm chỉ số cơ bản |
| period | string | Khoảng thời gian |

---

## 🗺️ Sơ đồ phụ thuộc tham số

```
┌─────────────────────────────────────────────────────────────┐
│  1. REFERENCE DATA  (Gọi đầu tiên)                         │
│                                                             │
│  equity/list ──→ {symbol} ──┬→ Market equity OHLCV/quote    │
│  equity/by-group            │→ Fundamental reports/ratios   │
│  equity/by-exchange         │→ Technical indicators         │
│                             │→ Company info/news/events     │
│                             └→ Screener (symbols param)     │
│                                                             │
│  index/list ────→ {index} ──┬→ Market index OHLCV           │
│                             └→ index/{index}/members        │
│                                                             │
│  futures/list ──→ {symbol} ─→ Futures OHLCV/quote/trades    │
│  warrants/list ─→ {symbol} ─→ Warrants OHLCV/quote         │
│  etf/list ──────→ {symbol} ─→ ETF OHLCV/quote              │
│  funds/list ────→ {fund_code} → Fund NAV/holdings           │
│                                                             │
│  Macro (gold, exchange-rate) ──→ Không cần tham số          │
│  Forex/Crypto/Commodity OHLCV ─→ Tham số tự do (pair)      │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔐 Cấu hình môi trường

Kết nối VNSTOCK qua tệp `.env`. Hỗ trợ nhiều API Key tự động xoay vòng:
```bash
VNSTOCK_API_KEY=key1,key2,key3
```

---

## ⚠️ Error Handling

| HTTP Code | Mô tả |
|-----------|-------|
| **422** | Tham số không đúng kiểu hoặc thiếu |
| **500** | Lỗi nội bộ server hoặc lỗi từ vnstock |

```json
{
  "success": false,
  "data": [],
  "message": "Chi tiết thông điệp lỗi...",
  "timestamp": "2026-06-19T09:35:00.123456",
  "count": 0
}
```
