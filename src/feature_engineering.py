import pandas as pd
import numpy as np

"""
Thực hiện xây dựng bộ đặc trưng phục vụ dự báo doanh thu, kết hợp giữa:
(1) đặc trưng chuỗi thời gian và (2) đặc trưng nghiệp vụ đa nguồn dữ liệu.

1. Time-series features:
- Thông tin thời gian (year, month, day, week, quarter, weekday)
- Biến nhị phân (weekend, year parity)
- Fourier features để mô hình hóa mùa vụ
- Biến mục tiêu LogRevenue (log1p)
- Lag features (lag_7, lag_14)
- Rolling statistics (mean, std theo cửa sổ 7–30 ngày)

2. Auxiliary business features:
- Inventory: stockout, fill rate, sell-through rate (theo tháng)
- Returns: số lượng trả hàng theo ngày
- Web traffic: sessions và unique visitors theo ngày
- Shipping: phí vận chuyển và thời gian giao hàng trung bình

Mục tiêu:
- Nắm bắt xu hướng + mùa vụ + hành vi vận hành doanh nghiệp
- Tăng sức mạnh dự báo cho các mô hình ML và Hybrid forecasting
"""

def engineer_features(df):

    df = df.copy()

    df = df.sort_values("Date")

    # =====================================
    # DATE FEATURES
    # =====================================

    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Day'] = df['Date'].dt.day

    df['DayOfWeek'] = df['Date'].dt.dayofweek
    df['DayOfYear'] = df['Date'].dt.dayofyear

    df['Quarter'] = df['Date'].dt.quarter

    df['WeekOfYear'] = (
    df['Date']
    .dt
    .isocalendar()
    .week
    .values          # ← THÊM DÒNG NÀY
    .astype(int)
)

    df['IsWeekend'] = (
        df['DayOfWeek'] >= 5
    ).astype(int)

    df['IsOddYear'] = (
        df['Year'] % 2
    ).astype(int)

    # =====================================
    # FOURIER FEATURES
    # =====================================

    df['doy_sin'] = np.sin(
        2 * np.pi * df['DayOfYear'] / 365.25
    )

    df['doy_cos'] = np.cos(
        2 * np.pi * df['DayOfYear'] / 365.25
    )

    df['dom_sin'] = np.sin(
        2 * np.pi * df['Day'] / 31
    )

    df['dom_cos'] = np.cos(
        2 * np.pi * df['Day'] / 31
    )

    df['dow_sin'] = np.sin(
        2 * np.pi * df['DayOfWeek'] / 7
    )

    df['dow_cos'] = np.cos(
        2 * np.pi * df['DayOfWeek'] / 7
    )

    df['month_sin'] = np.sin(
        2 * np.pi * df['Month'] / 12
    )

    df['month_cos'] = np.cos(
        2 * np.pi * df['Month'] / 12
    )

    # =====================================
    # TARGET TRANSFORM
    # =====================================

    if "LogRevenue" not in df.columns:
        df["LogRevenue"] = np.log1p(df["Revenue"])

    # =====================================
    # LAG FEATURES
    # =====================================

    df["lag_7"] = (
        df["LogRevenue"]
        .shift(7)
    )

    df["lag_14"] = (
        df["LogRevenue"]
        .shift(14)
    )

    # =====================================
    # MOVING AVERAGE FEATURES
    # =====================================

    df["ma_7"] = (
        df["LogRevenue"]
        .shift(1)
        .rolling(7)
        .mean()
    )

    df["ma_30"] = (
        df["LogRevenue"]
        .shift(1)
        .rolling(30)
        .mean()
    )

    # =====================================
    # ROLLING STD
    # =====================================

    df["std_30"] = (
        df["LogRevenue"]
        .shift(1)
        .rolling(30)
        .std()
    )

    return df


def build_aux_features(
    inventory_train,
    returns_train,
    web_train,
    shipments_train
):

    # =========================
    # INVENTORY
    # =========================
    inventory_train = inventory_train.copy()
    inventory_train["snapshot_date"] = pd.to_datetime(inventory_train["snapshot_date"])

    inventory_train["Month"] = inventory_train["snapshot_date"].dt.month

    inv_m = inventory_train.groupby("Month").agg({
        "stockout_days": "mean",
        "fill_rate": "mean",
        "sell_through_rate": "mean"
    })

    inv_m.columns = ["inv_stockout", "inv_fillrate", "inv_sellthru"]

    # =========================
    # RETURNS
    # =========================
    returns_train = returns_train.copy()
    returns_train["return_date"] = pd.to_datetime(returns_train["return_date"])

    returns_train["Month"] = returns_train["return_date"].dt.month
    returns_train["Day"] = returns_train["return_date"].dt.day

    ret_md = returns_train.groupby(["Month", "Day"]).size().to_frame("returns_md")

    # =========================
    # WEB
    # =========================
    web_train = web_train.copy()
    web_train["date"] = pd.to_datetime(web_train["date"])

    web_train["Month"] = web_train["date"].dt.month
    web_train["Day"] = web_train["date"].dt.day

    wt_md = web_train.groupby(["Month", "Day"]).agg({
        "sessions": "mean",
        "unique_visitors": "mean"
    })

    wt_md.columns = ["sessions_md", "visitors_md"]

    # =========================
    # SHIPPING
    # =========================
    shipments_train = shipments_train.copy()

    shipments_train["ship_date"] = pd.to_datetime(shipments_train["ship_date"])
    shipments_train["delivery_date"] = pd.to_datetime(shipments_train["delivery_date"])

    shipments_train["Month"] = shipments_train["ship_date"].dt.month
    shipments_train["Day"] = shipments_train["ship_date"].dt.day

    shipments_train["delivery_days"] = (
        (shipments_train["delivery_date"] - shipments_train["ship_date"])
        .dt.total_seconds() / 86400
    )

    ship_md = shipments_train.groupby(["Month", "Day"]).agg({
        "shipping_fee": "mean",
        "delivery_days": "mean"
    })

    ship_md.columns = ["avg_ship_fee", "avg_delivery_days"]

    return {
        "inv_m": inv_m,
        "ret_md": ret_md,
        "wt_md": wt_md,
        "ship_md": ship_md
    }