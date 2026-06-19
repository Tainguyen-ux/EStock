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
*   `data` (array|object): Dữ liệu kết quả thực tế từ API (thường là một danh sách các bản ghi hoặc một đối tượng duy nhất).
*   `message` (string): Thông báo từ hệ thống hoặc thông báo lỗi nếu `success` là `false`.
*   `timestamp` (string): Thời gian thực thi request dạng ISO-8601.
*   `count` (integer|null): Số lượng bản ghi trong mảng `data`.

---

## 🔧 System Endpoints — Nhóm Hệ thống

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/` | Thông tin cơ bản về hệ thống EStock API |
| GET | `/health` | Kiểm tra trạng thái hoạt động (Health check) & Thống kê Cache |
| POST | `/cache/clear` | Xóa toàn bộ dữ liệu lưu trong bộ nhớ đệm (Cache) |

### Ví dụ `/health` Response:
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "cache": {
      "hits": 124,
      "misses": 12,
      "size": 12
    }
  },
  "message": "OK",
  "timestamp": "2026-06-18T14:30:00.123456",
  "count": 1
}
```

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
    "percent_change": -0.968,
    "bid_price_1": 71600,
    "bid_vol_1": 676500,
    "ask_price_1": 71700,
    "ask_vol_1": 216600,
    "foreign_buy_volume": 836613,
    "foreign_sell_volume": 7822974,
    "foreign_room": 333823290
  }
]
```

### 1.2 OHLCV Cổ phiếu
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

**Ví dụ dữ liệu:**
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

### 1.3 Quote Real-time Cổ phiếu
```http
GET /api/market/equity/{symbol}/quote
```
*   **Mô tả**: Trả về dữ liệu quote real-time cho duy nhất một mã cổ phiếu được chỉ định. Cấu trúc tương tự như phần **1.1**.

### 1.4 Dữ liệu khớp lệnh tick-by-tick
```http
GET /api/market/equity/{symbol}/trades
```
*   **Mô tả**: Lấy chi tiết lịch sử khớp lệnh tick-by-tick trong ngày.
*   **Ví dụ dữ liệu:**
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

### 1.5 OHLCV Chỉ số Thị trường
```http
GET /api/market/index/{index}/ohlcv
```
*   **Params**: Tương tự OHLCV cổ phiếu. `{index}` có thể là `VNINDEX`, `HNXINDEX`, `UPINDEX`.

### 1.6 OHLCV Ngoại hối (Forex)
```http
GET /api/market/forex/{pair}/ohlcv
```
*   **Params**: Tương tự OHLCV cổ phiếu. `{pair}` là cặp ngoại tệ, ví dụ: `USDVND`, `EURVND`.

### 1.7 OHLCV Crypto
```http
GET /api/market/crypto/{pair}/ohlcv
```
*   **Params**: Tương tự OHLCV cổ phiếu. `{pair}` là cặp tiền mã hóa, ví dụ: `BTCUSD`, `ETHUSD`.

### 1.8 OHLCV Hàng hóa (Commodity)
```http
GET /api/market/commodity/{symbol}/ohlcv
```
*   **Params**: Tương tự OHLCV cổ phiếu. `{symbol}` là ký hiệu hàng hóa, ví dụ: `XAUUSD` (Vàng thế giới), `WTI` (Dầu thô).

---

## 📋 2. Reference Data — Dữ liệu Tham chiếu

### 2.1 Nhóm Danh sách Niêm yết
*   `GET /api/reference/equity/list`: Tất cả mã niêm yết trên thị trường.
*   `GET /api/reference/equity/by-group?group=VN30`: Lọc theo nhóm chỉ định (`VN30`, `HNX30`, `VNMidCap`...).
*   `GET /api/reference/equity/by-exchange?exchange=HOSE`: Lọc theo sàn giao dịch (`HOSE`, `HNX`, `UPCOM`).
*   `GET /api/reference/equity/by-industry`: Lấy danh sách mã chứng khoán phân nhóm theo bảng phân ngành ICB cấp 4.

### 2.2 Nhóm Thông tin Doanh nghiệp chi tiết
*   `GET /api/reference/company/{symbol}/info`: Lấy thông tin cơ bản của doanh nghiệp (Vốn điều lệ, số lao động, ban giám đốc, địa chỉ, website, email...).
*   `GET /api/reference/company/{symbol}/shareholders`: Danh sách cổ đông lớn kèm số lượng và tỷ lệ sở hữu.
*   `GET /api/reference/company/{symbol}/officers`: Danh sách ban lãnh đạo chủ chốt cùng chức vụ nắm giữ.
*   `GET /api/reference/company/{symbol}/subsidiaries`: Danh sách các công ty con, công ty liên kết của doanh nghiệp.
*   `GET /api/reference/company/{symbol}/ownership`: Cơ cấu sở hữu (Nhà nước, Khối ngoại, Cổ đông nội bộ...).
*   `GET /api/reference/company/{symbol}/insider-trading`: Lịch sử giao dịch nội bộ của ban lãnh đạo và người có liên quan.
*   `GET /api/reference/company/{symbol}/capital-history`: Lịch sử thay đổi và phát hành tăng vốn điều lệ.
*   `GET /api/reference/company/{symbol}/news`: Tin tức báo chí cập nhật liên quan đến doanh nghiệp.
    *   **Cấu trúc dữ liệu trong `data`**:
        ```json
        [
          {
            "title": "Theo dấu dòng tiền cá mập 18/06: MSB hút tiền tự doanh, FPT bị khối ngoại xả mạnh",
            "head": "Khối ngoại bán ròng gần 1.9 ngàn tỷ đồng...",
            "publish_time": "2026-06-18 19:02:00",
            "url": "https://kbbuddywts.kbsec.com.vn/2026/06/...",
            "article_id": 1455969
          }
        ]
        ```
*   `GET /api/reference/company/{symbol}/events`: Sự kiện chi trả cổ tức, họp ĐHĐCĐ sắp tới.

### 2.3 Nhóm Chỉ số (Index)
*   `GET /api/reference/index/list`: Danh sách tất cả chỉ số thị trường.
*   `GET /api/reference/index/groups`: Danh sách các nhóm chỉ số hỗ trợ.
*   `GET /api/reference/index/info`: Metadata thông số kỹ thuật của các chỉ số.
*   `GET /api/reference/index/{index}/members`: Danh sách các mã cổ phiếu thành phần (Ví dụ rổ thành phần `VN30` gồm 30 mã).

### 2.4 Nhóm Ngành (Industry)
*   `GET /api/reference/industry/list`: Cây danh mục phân ngành ICB.
*   `GET /api/reference/industry/sectors`: Danh sách mã cổ phiếu được phân nhóm vào từng ngành tương ứng.

### 2.5 Nhóm Tìm kiếm & Trạng thái
*   `GET /api/reference/search?query=FPT`: Tìm kiếm nhanh mã chứng khoán và thông tin liên quan.
*   `GET /api/reference/search/info?query=FPT`: Tìm kiếm thông tin chi tiết của tài sản.
*   `GET /api/reference/market/status`: Lấy trạng thái hoạt động thực tế của phiên giao dịch (`OPEN`, `CLOSED`, `LUNCH_BREAK`).

---

## 💰 3. Fundamental Data — Báo cáo & Chỉ số Tài chính

### 3.1 Báo cáo tài chính doanh nghiệp
*   `GET /api/fundamental/{symbol}/balance-sheet` (Bảng cân đối kế toán)
*   `GET /api/fundamental/{symbol}/income-statement` (Báo cáo kết quả HĐKD)
*   `GET /api/fundamental/{symbol}/cash-flow` (Báo cáo lưu chuyển tiền tệ)

| Param | Type | Default | Mô tả |
|-------|------|---------|-------|
| period | query | "year" | Lọc theo năm (`year`) hoặc theo quý (`quarter`). |

**Ví dụ cấu trúc dữ liệu:**
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

### 3.2 Chỉ số tài chính cơ bản (Ratios)
```http
GET /api/fundamental/{symbol}/ratios
```
*   **Mô tả**: Trả về các chỉ số tài chính cơ bản như P/E, P/B, EPS, ROE, ROA, biên lợi nhuận qua các kỳ báo cáo.

---

## 🔍 4. Stock Screener — Bộ lọc Cổ phiếu

### 4.1 Lọc theo Phân tích Cơ bản (FA)
```http
POST /api/screener/fundamental
```
**Request Body parameters:**
*   `exchange` (string, optional): Sàn giao dịch lọc.
*   `group` (string, optional): Nhóm chỉ số lọc (e.g. `VN30`).
*   `pe_min` / `pe_max` (float, optional): Khoảng P/E.
*   `pb_min` / `pb_max` (float, optional): Khoảng P/B.
*   `roe_min` / `roa_min` (float, optional): Tỷ lệ ROE / ROA tối thiểu (%).
*   `gross_margin_min` / `net_margin_min` (float, optional): Biên lợi nhuận tối thiểu (%).
*   `debt_equity_max` (float, optional): Tỷ lệ Nợ/Vốn CSH tối đa.
*   `revenue_growth_min` / `profit_growth_min` (float, optional): Tăng trưởng doanh thu/lợi nhuận tối thiểu (%).

### 4.2 Lọc theo Phân tích Kỹ thuật (TA)
```http
POST /api/screener/technical
```
**Request Body parameters:**
*   `symbols` (array of strings, optional): Tập hợp mã chứng khoán cần lọc.
*   `group` (string, optional): Nhóm chỉ số lọc.
*   `lookback_days` (integer): Số phiên lịch sử để đánh giá tín hiệu.
*   `ma_cross_up` / `ma_cross_down` (boolean, optional): MA20 cắt lên/cắt xuống MA50.
*   `above_ma20` / `above_ma50` (boolean, optional): Giá nằm trên MA20 / MA50.
*   `rsi_oversold` / `rsi_overbought` (boolean, optional): RSI quá bán (<30) / quá mua (>70).
*   `volume_spike` (boolean, optional): Đột biến khối lượng giao dịch.
*   `volume_spike_ratio` (float, optional): Tỷ số đột biến khối lượng (mặc định 2.0).
*   `macd_cross_up` (boolean, optional): MACD cắt lên Signal Line.

### 4.3 So sánh nhiều mã (Compare Side-by-side)
```http
POST /api/screener/compare
```
**Request Body parameters:**
*   `symbols` (array of strings): Danh sách các mã cần so sánh (e.g., `["FPT", "TCB", "VCB"]`).
*   `include_price` (boolean): Bao gồm dữ liệu giá đóng cửa mới nhất.
*   `include_fundamental` (boolean): Bao gồm chỉ số cơ bản (ROE, P/E, EPS, ...).
*   `period` (string): Khoảng thời gian lấy dữ liệu.

---

## 🌍 5. Macro Data — Dữ liệu Vĩ mô

### 5.1 Giá vàng trong nước
```http
GET /api/macro/gold
```
| Param | Type | Default | Mô tả |
|-------|------|---------|-------|
| source | query | "sjc" | Nguồn giá vàng: `sjc`, `doji` hoặc `pnj`. |

### 5.2 Tỷ giá ngoại tệ Vietcombank
```http
GET /api/macro/exchange-rate
```
*   **Mô tả**: Trả về bảng tỷ giá mua tiền mặt, mua chuyển khoản và giá bán ra của các loại ngoại tệ giao dịch tại Vietcombank.

### 5.3 Lịch sử tỷ giá ngoại hối
```http
GET /api/macro/forex/{pair}/ohlcv
```
*   **Params**: Tương tự OHLCV cổ phiếu. `{pair}` là cặp tỷ giá ngoại hối (Ví dụ: `USDVND`, `EURVND`).

---

## 🔐 6. Derivatives — Chứng khoán Phái sinh & ETF

### 6.1 Nhóm Hợp đồng Tương lai (Futures)
*   `GET /api/derivatives/futures/list`: Lấy danh sách mã hợp đồng tương lai đang lưu hành.
*   `GET /api/derivatives/futures/info`: Thông số cấu trúc chi tiết của các hợp đồng tương lai.
*   `GET /api/derivatives/futures/{symbol}/ohlcv`: Dữ liệu lịch sử nến của hợp đồng phái sinh chỉ định.
*   `GET /api/derivatives/futures/{symbol}/quote`: Giá real-time của hợp đồng tương lai.
*   `GET /api/derivatives/futures/{symbol}/trades`: Nhật ký lịch sử khớp lệnh tick-by-tick của hợp đồng tương lai.

### 6.2 Nhóm Chứng quyền có bảo đảm (Covered Warrants)
*   `GET /api/derivatives/warrants/list`: Lấy danh sách tất cả mã chứng quyền niêm yết.
*   `GET /api/derivatives/warrants/info`: Metadata thông số kỹ thuật của chứng quyền (Tỷ lệ chuyển đổi, giá thực hiện, ngày đáo hạn, tổ chức phát hành...).
*   `GET /api/derivatives/warrants/{symbol}/ohlcv`: Dữ liệu lịch sử nến chứng quyền.
*   `GET /api/derivatives/warrants/{symbol}/quote`: Bảng giá real-time của chứng quyền.

### 6.3 Nhóm Quỹ ETF
*   `GET /api/derivatives/etf/list`: Lấy danh sách tất cả các quỹ ETF niêm yết.
*   `GET /api/derivatives/etf/{symbol}/ohlcv`: Dữ liệu lịch sử nến của quỹ ETF.
*   `GET /api/derivatives/etf/{symbol}/quote`: Bảng giá real-time của quỹ ETF.

---

## 🏦 7. Investment Funds — Quỹ đầu tư mở

*   `GET /api/funds/list`: Lấy danh sách toàn bộ các quỹ đầu tư mở đăng ký tại Việt Nam.
*   `GET /api/funds/{fund_code}/nav`: Lịch sử biến động NAV/Chứng chỉ quỹ của quỹ chỉ định.
*   `GET /api/funds/{fund_code}/top-holding`: Danh sách các tài sản / cổ phiếu nắm giữ lớn nhất trong danh mục quỹ.
*   `GET /api/funds/{fund_code}/industry-holding`: Phân bổ tỷ lệ đầu tư của danh mục theo nhóm ngành.
*   `GET /api/funds/{fund_code}/asset-holding`: Phân bổ tỷ trọng đầu tư theo phân lớp tài sản (Cổ phiếu, tiền mặt, trái phiếu...).

---

## 📉 8. Technical Analysis — Phân tích Kỹ thuật

### 8.1 Tất cả chỉ báo kỹ thuật tổng hợp
```http
GET /api/technical/{symbol}/indicators
```
| Param | Type | Default | Mô tả |
|-------|------|---------|-------|
| length | query | 200 | Số phiên lịch sử lấy về để tính chỉ báo |
| sma_periods | query | "5,10,20,50,200" | Danh sách các chu kỳ tính đường SMA |
| ema_periods | query | "12,26" | Danh sách các chu kỳ tính đường EMA |
| rsi_period | query | 14 | Chu kỳ tính toán RSI |

### 8.2 Các Endpoint Chỉ báo Riêng lẻ
Các endpoint này trả về nến OHLCV kèm theo duy nhất dữ liệu tính toán của chỉ báo tương ứng để giảm thiểu kích thước payload phản hồi:

*   `GET /api/technical/{symbol}/sma`: Simple Moving Average.
    *   *Params*: `period` (default: 20), `length` (default: 100).
*   `GET /api/technical/{symbol}/ema`: Exponential Moving Average.
    *   *Params*: `period` (default: 20), `length` (default: 100).
*   `GET /api/technical/{symbol}/rsi`: Relative Strength Index.
    *   *Params*: `period` (default: 14), `length` (default: 100).
*   `GET /api/technical/{symbol}/macd`: Moving Average Convergence Divergence.
    *   *Params*: `fast` (default: 12), `slow` (default: 26), `signal` (default: 9), `length` (default: 100).
*   `GET /api/technical/{symbol}/bollinger`: Bollinger Bands.
    *   *Params*: `period` (default: 20), `std_dev` (default: 2.0), `length` (default: 100).
*   `GET /api/technical/{symbol}/stochastic`: Stochastic Oscillator.
    *   *Params*: `k_period` (default: 14), `d_period` (default: 3), `length` (default: 100).
*   `GET /api/technical/{symbol}/atr`: Average True Range.
    *   *Params*: `period` (default: 14), `length` (default: 100).

---

## 🔐 Cấu hình môi trường

Tất cả các kết nối đến VNSTOCK được cấu hình trực tiếp thông qua tệp tin `.env` trên máy chủ. Hệ thống hỗ trợ cấu hình nhiều API Key phân tách bằng dấu phẩy để tự động xoay vòng (rotation) khi gặp lỗi giới hạn lượt gọi (rate-limit) hoặc lỗi kết nối:
```bash
VNSTOCK_API_KEY=key1,key2,key3
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
