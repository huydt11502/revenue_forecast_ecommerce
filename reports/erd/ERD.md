# Sơ đồ ERD — Hệ thống Thương mại điện tử Thời trang

> Dùng cho **Phần 2 — Chương 2.3 (Mô hình dữ liệu)** của báo cáo.
> Sơ đồ Mermaid bên dưới render trực tiếp trên GitHub, VS Code (Markdown Preview Mermaid), hoặc https://mermaid.live

## 1. Sơ đồ quan hệ thực thể (ERD)

```mermaid
erDiagram
    GEOGRAPHY  ||--o{ CUSTOMERS   : "zip"
    GEOGRAPHY  ||--o{ ORDERS      : "zip"
    CUSTOMERS  ||--o{ ORDERS      : "customer_id"
    CUSTOMERS  ||--o{ REVIEWS     : "customer_id"

    ORDERS     ||--|{ ORDER_ITEMS : "order_id"
    ORDERS     ||--o| PAYMENTS    : "order_id"
    ORDERS     ||--o| SHIPMENTS   : "order_id"
    ORDERS     ||--o{ RETURNS     : "order_id"
    ORDERS     ||--o{ REVIEWS     : "order_id"

    PRODUCTS   ||--o{ ORDER_ITEMS : "product_id"
    PRODUCTS   ||--o{ RETURNS     : "product_id"
    PRODUCTS   ||--o{ REVIEWS     : "product_id"
    PRODUCTS   ||--o{ INVENTORY   : "product_id"

    PROMOTIONS ||--o{ ORDER_ITEMS : "promo_id"

    ORDERS     }o--|| SALES         : "order_date ~ Date"
    WEB_TRAFFIC ||--o| SALES        : "date ~ Date"

    GEOGRAPHY {
        int    zip PK
        string city
        string region
        string district
    }

    CUSTOMERS {
        int    customer_id PK
        int    zip FK
        string city
        date   signup_date
        string gender
        string age_group
        string acquisition_channel
    }

    PRODUCTS {
        int    product_id PK
        string product_name
        string category
        string segment
        string size
        string color
        float  price
        float  cogs
    }

    PROMOTIONS {
        string promo_id PK
        string promo_name
        string promo_type
        float  discount_value
        date   start_date
        date   end_date
        string applicable_category
        string promo_channel
        int    stackable_flag
        float  min_order_value
    }

    ORDERS {
        int    order_id PK
        date   order_date
        int    customer_id FK
        int    zip FK
        string order_status
        string payment_method
        string device_type
        string order_source
    }

    ORDER_ITEMS {
        int    order_id FK
        int    product_id FK
        int    quantity
        float  unit_price
        float  discount_amount
        string promo_id FK
        string promo_id_2 FK
    }

    PAYMENTS {
        int    order_id FK
        string payment_method
        float  payment_value
        int    installments
    }

    SHIPMENTS {
        int    order_id FK
        date   ship_date
        date   delivery_date
        float  shipping_fee
    }

    RETURNS {
        string return_id PK
        int    order_id FK
        int    product_id FK
        date   return_date
        string return_reason
        int    return_quantity
        float  refund_amount
    }

    REVIEWS {
        string review_id PK
        int    order_id FK
        int    product_id FK
        int    customer_id FK
        date   review_date
        int    rating
        string review_title
    }

    INVENTORY {
        date   snapshot_date
        int    product_id FK
        int    stock_on_hand
        int    units_received
        int    units_sold
        int    stockout_days
        float  days_of_supply
        float  fill_rate
        int    stockout_flag
        int    overstock_flag
        int    reorder_flag
        float  sell_through_rate
    }

    SALES {
        date   Date PK
        float  Revenue
        float  COGS
    }

    WEB_TRAFFIC {
        date   date PK
        int    sessions
        int    unique_visitors
        int    page_views
        float  bounce_rate
        float  avg_session_duration_sec
        string traffic_source
    }
```

## 2. Mô tả quan hệ giữa các bảng

### Nhóm Master (dữ liệu chủ)

| Quan hệ | Loại | Khóa | Ý nghĩa |
|---------|------|------|---------|
| GEOGRAPHY → CUSTOMERS | 1 : N | `zip` | Mỗi khu vực (zip) có nhiều khách hàng |
| GEOGRAPHY → ORDERS | 1 : N | `zip` | Mỗi khu vực có nhiều đơn hàng giao đến |

### Nhóm Transaction (giao dịch)

| Quan hệ | Loại | Khóa | Ý nghĩa |
|---------|------|------|---------|
| CUSTOMERS → ORDERS | 1 : N | `customer_id` | Một khách hàng đặt nhiều đơn |
| ORDERS → ORDER_ITEMS | 1 : N | `order_id` | Một đơn gồm nhiều dòng sản phẩm |
| PRODUCTS → ORDER_ITEMS | 1 : N | `product_id` | Một sản phẩm xuất hiện ở nhiều dòng đơn |
| PROMOTIONS → ORDER_ITEMS | 1 : N | `promo_id`, `promo_id_2` | Một KM áp cho nhiều dòng đơn (có thể stack 2 KM) |
| ORDERS → PAYMENTS | 1 : 1 | `order_id` | Mỗi đơn có một bản ghi thanh toán |
| ORDERS → SHIPMENTS | 1 : 1 | `order_id` | Mỗi đơn có một lần giao hàng |
| ORDERS → RETURNS | 1 : N | `order_id` | Một đơn có thể trả nhiều sản phẩm |
| ORDERS → REVIEWS | 1 : N | `order_id` | Một đơn có thể có nhiều đánh giá |
| PRODUCTS → RETURNS / REVIEWS | 1 : N | `product_id` | Sản phẩm bị trả / được đánh giá nhiều lần |
| CUSTOMERS → REVIEWS | 1 : N | `customer_id` | Một khách viết nhiều đánh giá |

### Nhóm Operational & Analytical

| Quan hệ | Loại | Khóa | Ý nghĩa |
|---------|------|------|---------|
| PRODUCTS → INVENTORY | 1 : N | `product_id` | Mỗi sản phẩm có nhiều bản ghi tồn kho theo tháng (`snapshot_date`) |
| ORDERS → SALES | N : 1 | `order_date` ≈ `Date` | **SALES là bảng tổng hợp doanh thu theo ngày**, được suy ra từ ORDER_ITEMS/ORDERS |
| WEB_TRAFFIC → SALES | 1 : 1 | `date` ≈ `Date` | Lưu lượng web theo ngày, ghép với doanh thu theo ngày |

### Ghi chú quan trọng cho mô hình dự báo

- **`SALES.csv`** (target) là dữ liệu **tổng hợp theo ngày** (`Date`, `Revenue`, `COGS`) — không có khóa ngoại trực tiếp, mà là kết quả roll-up từ các bảng giao dịch.
- **`sample_submission.csv`** có cùng cấu trúc `SALES` — dùng làm khung nộp Kaggle (giai đoạn test 2023→2024).
- Cầu nối để tạo feature: ghép theo **trục thời gian (ngày)** giữa `SALES` ↔ `WEB_TRAFFIC` ↔ `PROMOTIONS` (theo khoảng `start_date`–`end_date`) ↔ `INVENTORY` (theo `snapshot_date`) ↔ tổng hợp `ORDERS`/`RETURNS` theo ngày.

## 3. Phiên bản DBML (cho dbdiagram.io)

> Copy nội dung file [`schema.dbml`](schema.dbml) dán vào https://dbdiagram.io để xuất ảnh ERD chất lượng cao đưa vào báo cáo/slide.
