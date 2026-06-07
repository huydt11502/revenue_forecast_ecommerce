# Dự Báo Doanh Thu - Thương Mại Điện Tử Thời Trang

Báo cáo kiến tập | Nguồn dữ liệu: Datathon 2026 - The Gridbreakers

## Mô tả bài toán

Doanh nghiệp thương mại điện tử thời trang tại Việt Nam cần dự báo doanh thu (Revenue) để tối ưu tồn kho, lập kế hoạch khuyến mãi và vận hành logistics.

- **Train**: `sales.csv` — 04/07/2012 đến 31/12/2020
- **Test**: `sales_test.csv` — 01/01/2021 đến 31/12/2022
- **Metric**: MAE, RMSE, R², Adjusted R-Square

## Cấu trúc dự án

```
revenue-forecast-ecommerce/
├── data/
│   ├── raw/              # 15 CSV files gốc, không chỉnh sửa
│   │   ├── master/       # products, customers, promotions, geography
│   │   ├── transaction/  # orders, order_items, payments, shipments, returns, reviews
│   │   ├── analytical/   # sales, sales_test, sample_submission
│   │   └── operational/  # inventory, web_traffic
│   └── processed/
│       ├── cleaned/      # Data sau làm sạch
│       └── features/     # Feature table cho modeling
├── notebooks/            # Jupyter Notebooks — thực hiện theo thứ tự
│   ├── 01_data_overview.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_eda_master.ipynb
│   ├── 04_eda_operations.ipynb
│   ├── 05_business_analysis.ipynb
│   ├── 06_time_series_decomposition.ipynb
│   ├── 07_modeling.ipynb
├── src/                  # Utility functions tái sử dụng
│   ├── data_loader.py
│   ├── preprocessing.py
│   ├── feature_engineering.py
│   └── evaluation.py
├── outputs/
│   ├── figures/          # Biểu đồ export (PNG)
│   
├── reports/
│   └── powerbi/          # File .pbix dashboards
├── requirements.txt
└── README.md
```

## Hướng dẫn chạy

```bash
# 1. Cài đặt thư viện
pip install -r requirements.txt

# 2. Chạy notebooks theo thứ tự từ 01 đến 08
jupyter notebook
```

## Quy trình phân tích (CRISP-DM)

| Bước | Notebook | Nội dung |
|------|----------|----------|
| Data Understanding | 01 | Tổng quan 15 bảng dữ liệu |
| Data Preparation | 02 | Làm sạch, xử lý missing values |
| EDA | 03, 04 | Phân tích Master & Operations |
| Business Analysis | 05 | KPIs, vấn đề cốt lõi|
| Modeling | 06, 07 | STL decomposition, train, evaluate |

## Thành viên nhóm

- Thành viên 1: Lê Quang Huy
- Thành viên 2: Nguyễn Tấn Trọng

Giảng viên hướng dẫn: NCS.ThS Nguyễn Quang Phúc
