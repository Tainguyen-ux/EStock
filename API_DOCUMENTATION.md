# 📊 EStock API Documentation

## Tổng quan

**Base URL**: `http://34.87.142.4:8000`

**Định dạng phản hồi chung (Response Wrapper Schema)**:
Tất cả các endpoint trong hệ thống đều trả về cấu trúc JSON đồng nhất như sau:

```json
{
  "success": true,
  "data": [],
  "message": "Thông tin bổ sung hoặc thông điệp lỗi",
  "timestamp": "2026-06-18T14:30:00.123456",
  "count": 0
}
```

*   `success` (boolean): Trạng thái gọi API thành công (`true`) hay thất bại (`false`).
*   `data` (array|object): Dữ liệu kết quả thực tế từ API (thường là một danh sách các bản ghi).
*   `message` (string): Thông báo từ hệ thống hoặc thông báo lỗi nếu `success` là `false`.
*   `timestamp` (string): Thời gian thực thi request dạng ISO-8601.
*   `count` (integer|null): Số lượng bản ghi trong mảng `data`.

---

## 🔧 System Endpoints

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/` | Thông tin cơ bản về hệ thống EStock API |
| GET | `/health` | Kiểm tra trạng thái hoạt động (Health check) & Thống kê Cache |
| POST | `/cache/clear` | Xóa toàn bộ dữ liệu lưu trong bộ nhớ đệm (Cache) |

---

## 📈 1. Market Data — Dữ liệu Thị trường

### 1.1 Bảng giá toàn thị trường
```http
GET /api/market/quote
```
| Param | Type | Default | Mô tả |
|-------|------|---------|-------|
| symbols | query | "" | Danh sách mã chứng khoán (ví dụ: `FPT,TCB,VCB`). Để trống để lấy mặc định rổ VN30. |

**Cấu trúc dữ liệu trong `data` (Real-time Quote):**
```json
[
  {
    "symbol": "FPT",
    "time": 1781771587691,
    "exchange": "HOSE",
    "ceiling_price": 77300,
    "floor_price": 67300,
    "reference_price": 72300,
    "open_price": 72300,
    "high_price": 72300,
    "low_price": 71500,
    "close_price": 71600,
    "average_price": 71722,
    "volume_accumulated": 13665800,
    "total_value": 980132220000,
    "price_change": -700,
    "percent_change": -0.9681881051175657,
    "bid_price_1": "71600.0",
    "bid_vol_1": 676500,
    "bid_price_2": 71500,
    "bid_vol_2": 1220200,
    "bid_price_3": 71400,
    "bid_vol_3": 320800,
    "ask_price_1": "71700.0",
    "ask_vol_1": 216600,
    "ask_price_2": 71800,
    "ask_vol_2": 21000,
    "ask_price_3": 71900,
    "ask_vol_3": 13700,
    "foreign_buy_volume": 836613,
    "foreign_sell_volume": 7822974,
    "foreign_room": 333823290
  }
]
```
*   `ceiling_price` / `floor_price` / `reference_price`: Giá trần / sàn / tham chiếu (đơn vị: VNĐ).
*   `open_price` / `high_price` / `low_price` / `close_price`: Giá mở cửa / cao nhất / thấp nhất / giá khớp gần nhất.
*   `volume_accumulated`: Tổng khối lượng giao dịch tích lũy trong ngày.
*   `total_value`: Tổng giá trị giao dịch trong ngày (đơn vị: VNĐ).
*   `bid_price_x` / `bid_vol_x`: Giá mua và khối lượng dư mua tốt nhất ở mức ưu tiên thứ `x` (1 đến 3).
*   `ask_price_x` / `ask_vol_x`: Giá bán và khối lượng dư bán tốt nhất ở mức ưu tiên thứ `x` (1 đến 3).
*   `foreign_buy_volume` / `foreign_sell_volume`: Khối lượng khối ngoại mua / bán.
*   `foreign_room`: Số cổ phiếu còn lại khối ngoại được phép mua.

### 1.2 OHLCV cổ phiếu
```http
GET /api/market/equity/{symbol}/ohlcv
```
| Param | Type | Default | Mô tả |
|-------|------|---------|-------|
| symbol | path | required | Mã chứng khoán (ví dụ: `VCB`, `FPT`, `TCB`...) |
| start | query | "" | Ngày bắt đầu dạng YYYY-MM-DD |
| end | query | "" | Ngày kết thúc dạng YYYY-MM-DD |
| interval | query | "1D" | Khung thời gian: `1m`, `5m`, `15m`, `30m`, `1H`, `1D`, `1W`, `1M` |
| length | query | 90 | Số nến lịch sử lấy về (sử dụng khi không có `start` và `end`) |

**Cấu trúc dữ liệu trong `data` (OHLCV):**
```json
[
  {
    "time": "2026-06-17 07:00:00",
    "open": 73.3,
    "high": 73.4,
    "low": 72.2,
    "close": 72.3,
    "volume": 10652200
  }
]
```
*   `time`: Thời gian của nến.
*   `open` / `high` / `low` / `close`: Giá mở / cao / thấp / đóng cửa.
*   `volume`: Khối lượng giao dịch trong khung thời gian đó.

### 1.3 Quote real-time cổ phiếu
```http
GET /api/market/equity/{symbol}/quote
```
*   **Mô tả**: Trả về dữ liệu quote real-time cho duy nhất một mã cổ phiếu.
*   **Response**: Cấu trúc tương tự như phần **1.1** nhưng `data` chỉ chứa một bản ghi tương ứng của mã chứng khoán được chỉ định.

### 1.4 Dữ liệu khớp lệnh tick-by-tick
```http
GET /api/market/equity/{symbol}/trades
```
**Cấu trúc dữ liệu trong `data`:**
```json
[
  {
    "time": "2026-06-18 14:28:57",
    "price": 71.7,
    "volume": 500,
    "match_type": "buy",
    "id": "2026-06-18_142857_717000_500"
  }
]
```
*   `price`: Mức giá khớp lệnh (chia cho 1000 so với bảng giá gốc nếu hiển thị đơn vị điểm).
*   `match_type`: Loại chủ động khớp (`buy` - khớp mua chủ động, `sell` - khớp bán chủ động).
*   `id`: ID duy nhất của bước giá khớp lệnh.

### 1.5 OHLCV chỉ số thị trường
```http
GET /api/market/index/{index}/ohlcv
```
*   **Params**: Tương tự OHLCV cổ phiếu. `{index}` có thể là `VNINDEX`, `HNXINDEX`, `UPINDEX`.
*   **Response**: Trả về danh sách OHLCV lịch sử của chỉ số tương tự cấu trúc phần **1.2**.

---

## 📋 2. Reference Data — Dữ liệu Tham chiếu

### 2.1 Danh sách cổ phiếu niêm yết
*   `GET /api/reference/equity/list`: Tất cả mã niêm yết trên thị trường.
*   `GET /api/reference/equity/by-group?group=VN30`: Lấy theo nhóm chỉ định (`VN30`, `HNX30`, `VNMidCap`...).
*   `GET /api/reference/equity/by-exchange?exchange=HOSE`: Lấy theo sàn niêm yết (`HOSE`, `HNX`, `UPCOM`).

**Cấu trúc dữ liệu trong `data`:**
```json
[
  {
    "symbol": "FPT",
    "company_name": "Công ty Cổ phần FPT",
    "exchange": "HOSE",
    "industry": "Công nghệ thông tin"
  }
]
```

### 2.2 Thông tin doanh nghiệp
```http
GET /api/reference/company/{symbol}/info
```
**Cấu trúc dữ liệu trong `data`:**
```json
{
  "business_model": "Mô tả chi tiết về mô hình kinh doanh của doanh nghiệp...",
  "symbol": "FPT",
  "founded_date": "28/02/2002",
  "charter_capital": 17035,
  "number_of_employees": 54110,
  "listing_date": "13/12/2006",
  "par_value": 10000,
  "exchange": "HOSE",
  "listing_price": 400000,
  "listed_volume": 1704,
  "ceo_name": "Mr. Trương Gia Bình",
  "ceo_position": "Chủ tịch HĐQT",
  "inspector_name": "Ms. Mai Thị Lan Anh",
  "auditor": "Deloitte",
  "company_type": "Công ty cổ phần",
  "address": "Số 10 - Phố Phạm Văn Bạch - P. Cầu Giấy - Tp. Hà Nội",
  "phone": "(84.24) 7300 7300",
  "website": "https://fpt.com",
  "email": "Ir@fpt.com",
  "outstanding_shares": 1703507121
}
```
*   `charter_capital`: Vốn điều lệ (tính theo tỷ VNĐ).
*   `outstanding_shares`: Số lượng cổ phiếu đang lưu hành trên thị trường.

### 2.3 Danh sách cổ đông lớn
```http
GET /api/reference/company/{symbol}/shareholders
```
**Cấu trúc dữ liệu trong `data`:**
```json
[
  {
    "name": "Trương Gia Bình",
    "update_date": "2025-12-31T00:00:00",
    "shares_owned": 117347966,
    "ownership_percentage": 6.89
  }
]
```
*   `shares_owned`: Số cổ phiếu nắm giữ.
*   `ownership_percentage`: Tỷ lệ sở hữu tính theo phần trăm (%).

---

## 💰 3. Fundamental Data — Báo cáo & Chỉ số Tài chính

### 3.1 Báo cáo tài chính
*   `GET /api/fundamental/{symbol}/balance-sheet` (Bảng cân đối kế toán)
*   `GET /api/fundamental/{symbol}/income-statement` (Kết quả hoạt động kinh doanh)
*   `GET /api/fundamental/{symbol}/cash-flow` (Báo cáo lưu chuyển tiền tệ)

| Param | Type | Default | Mô tả |
|-------|------|---------|-------|
| period | query | "year" | Lọc theo năm (`year`) hoặc theo quý (`quarter`). |

**Cấu trúc dữ liệu trong `data`:**
```json
[
  {
    "item": "Tài sản ngắn hạn",
    "item_id": "short_term_assets",
    "2025": 28450122000000,
    "2024": 26110900000000,
    "2023": 23440100000000
  }
]
```

### 3.2 Chỉ số tài chính cơ bản (Ratios)
```http
GET /api/fundamental/{symbol}/ratios
```
**Cấu trúc dữ liệu trong `data`:**
```json
[
  {
    "item": "Thu nhập trên mỗi cổ phần của 4 quý gần nhất (EPS)",
    "item_id": "trailing_eps",
    "2025": 6021.21,
    "2024": 5703.67,
    "2023": 5471.26,
    "2022": 5251.94
  }
]
```
*   Các trường năm động (ví dụ `"2025"`, `"2024"`) biểu thị giá trị của chỉ số tại năm đó.
*   Các mã `item_id` phổ biến gồm: `trailing_eps` (EPS), `pe` (P/E), `pb` (P/B), `roe` (ROE), `roa` (ROA), `net_profit_margin` (Biên lợi nhuận ròng)...

---

## 🔍 4. Stock Screener — Bộ lọc Cổ phiếu

### 4.1 Lọc theo Phân tích Cơ bản (FA)
```http
POST /api/screener/fundamental
```
**Request Body:**
```json
{
  "exchange": "HOSE",
  "group": "VN30",
  "pe_max": 15,
  "roe_min": 15,
  "debt_equity_max": 1.5,
  "limit": 50
}
```
**Response**: Trả về danh sách thông tin và giá của các cổ phiếu thỏa mãn tiêu chí lọc.

### 4.2 Lọc theo Phân tích Kỹ thuật (TA)
```http
POST /api/screener/technical
```
**Request Body:**
```json
{
  "group": "VN30",
  "rsi_oversold": true,
  "volume_spike": true,
  "volume_spike_ratio": 2.0,
  "lookback_days": 60,
  "limit": 50
}
```
**Response**: Danh sách các cổ phiếu khớp tín hiệu kỹ thuật (ví dụ: RSI quá bán, đột biến Volume, MACD cắt lên...).

### 4.3 So sánh nhiều mã (Compare Side-by-side)
```http
POST /api/screener/compare
```
**Request Body:**
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

### 5.1 Giá vàng trong nước
```http
GET /api/macro/gold
```
| Param | Type | Default | Mô tả |
|-------|------|---------|-------|
| source | query | "sjc" | Nguồn giá vàng: `sjc`, `doji` hoặc `pnj`. |

**Cấu trúc dữ liệu trong `data`:**
```json
[
  {
    "name": "Vàng SJC 1L, 10L, 1KG",
    "branch": "Hồ Chí Minh",
    "buy_price": 148800000.0,
    "sell_price": 151300000.0,
    "date": "2026-06-18"
  }
]
```
*   `buy_price`: Giá mua vào của tiệm vàng (đơn vị: VNĐ/lượng).
*   `sell_price`: Giá bán ra cho khách hàng (đơn vị: VNĐ/lượng).

### 5.2 Tỷ giá ngoại tệ Vietcombank
```http
GET /api/macro/exchange-rate
```
**Cấu trúc dữ liệu trong `data`:**
```json
[
  {
    "currency_code": "USD",
    "currency_name": "US DOLLAR",
    "buy_cash": "25,120.00",
    "buy_transfer": "25,150.00",
    "sell": "25,480.00",
    "date": "2026-06-18"
  }
]
```

---

## 🏦 6. Investment Funds — Quỹ đầu tư

### 6.1 Lịch sử NAV của Quỹ mở
```http
GET /api/funds/{fund_code}/nav
```
**Cấu trúc dữ liệu trong `data`:**
```json
[
  {
    "date": "2026-06-18",
    "nav_per_share": 24512.82,
    "nav_change": 120.5,
    "nav_change_percentage": 0.49
  }
]
```

---

## 📉 7. Technical Analysis — Phân tích Kỹ thuật

### 7.1 Tất cả chỉ báo kỹ thuật tổng hợp
```http
GET /api/technical/{symbol}/indicators
```
| Param | Type | Default | Mô tả |
|-------|------|---------|-------|
| length | query | 200 | Số nến lịch sử lấy về để tính chỉ báo |
| sma_periods | query | "5,10,20,50,200" | Danh sách các chu kỳ tính đường SMA |
| ema_periods | query | "12,26" | Danh sách các chu kỳ tính đường EMA |
| rsi_period | query | 14 | Chu kỳ tính toán RSI |

**Cấu trúc dữ liệu trong `data`:**
```json
[
  {
    "time": "2026-06-18 07:00:00",
    "open": 72.3,
    "high": 72.3,
    "low": 71.5,
    "close": 71.6,
    "volume": 13665800,
    "sma_5": 72.84,
    "sma_10": 73.31,
    "sma_20": 73.4435,
    "ema_12": 73.1515,
    "ema_26": 73.0614,
    "rsi": 43.5554,
    "macd": 0.0901,
    "macd_signal": 0.429,
    "macd_histogram": -0.339,
    "bb_upper": 76.2436,
    "bb_middle": 73.4435,
    "bb_lower": 70.6434,
    "stoch_k": 1.6129,
    "stoch_d": 19.3782,
    "atr": 1.6522,
    "volume_sma_20": 9640255.0,
    "volume_ratio": 1.4176
  }
]
```
*   `sma_{x}`: Giá trị đường Simple Moving Average tại chu kỳ `x`.
*   `ema_{x}`: Giá trị đường Exponential Moving Average tại chu kỳ `x`.
*   `rsi`: Chỉ số Sức mạnh tương đối (RSI).
*   `macd` / `macd_signal` / `macd_histogram`: Dữ liệu phân kỳ hội tụ trung bình động (MACD).
*   `bb_upper` / `bb_middle` / `bb_lower`: Dải trên, giữa (trung bình SMA20), và dải dưới của chỉ báo Bollinger Bands.
*   `stoch_k` / `stoch_d`: Đường nhanh %K và đường chậm %D của Stochastic Oscillator.
*   `atr`: Average True Range đo lường độ biến động của thị trường.
*   `volume_sma_20`: Khối lượng giao dịch trung bình 20 phiên.
*   `volume_ratio`: Tỷ lệ đột biến khối lượng (Ví dụ: `1.4` nghĩa là volume phiên này gấp `1.4` lần trung bình 20 phiên).

---

## 🔐 Xác thực & Cấu hình môi trường

Tất cả các kết nối đến VNSTOCK được cấu hình trực tiếp thông qua tệp tin `.env` trên máy chủ:
```bash
VNSTOCK_API_KEY=vnstock_16c02b705fa4867320800e7d168863de
```

---

## ⚠️ Error Handling

Khi có lỗi xảy ra (ví dụ: sai tham số truy vấn hoặc lỗi kết nối đến API Vnstock), hệ thống sẽ phản hồi bằng mã trạng thái HTTP thích hợp:

*   **422 Unprocessable Entity**: Tham số truyền lên không đúng kiểu dữ liệu hoặc bị thiếu.
*   **500 Internal Server Error**: Lỗi phát sinh trong quá trình tính toán hoặc lỗi trả về từ server của vnstock.

```json
{
  "success": false,
  "data": [],
  "message": "Chi tiết thông điệp lỗi tại đây...",
  "timestamp": "2026-06-18T14:35:00.123456",
  "count": 0
}
```
