import pandas as pd
import numpy as np


def add_time_features(df: pd.DataFrame, date_col: str) -> pd.DataFrame:
    """Thêm các feature thời gian từ cột date."""
    df = df.copy()
    dt = df[date_col]
    df["year"]       = dt.dt.year
    df["month"]      = dt.dt.month
    df["quarter"]    = dt.dt.quarter
    df["dayofweek"]  = dt.dt.dayofweek
    df["dayofyear"]  = dt.dt.dayofyear
    df["weekofyear"] = dt.dt.isocalendar().week.astype(int)
    df["is_weekend"] = (dt.dt.dayofweek >= 5).astype(int)
    return df


def add_lag_features(df: pd.DataFrame, target_col: str, lags: list[int]) -> pd.DataFrame:
    """Thêm lag features cho cột target (cần sort theo thời gian trước)."""
    df = df.copy()
    for lag in lags:
        df[f"{target_col}_lag_{lag}"] = df[target_col].shift(lag)
    return df


def add_rolling_features(
    df: pd.DataFrame,
    target_col: str,
    windows: list[int],
    funcs: list[str] = ["mean", "std", "min", "max"],
) -> pd.DataFrame:
    """Thêm rolling statistics (mean, std, min, max) cho cột target."""
    df = df.copy()
    for w in windows:
        for f in funcs:
            col_name = f"{target_col}_rolling_{w}_{f}"
            df[col_name] = df[target_col].shift(1).rolling(w).agg(f)
    return df


def add_promotion_flags(df: pd.DataFrame, promotions: pd.DataFrame, date_col: str) -> pd.DataFrame:
    """Đánh dấu các ngày có chương trình khuyến mãi đang chạy."""
    df = df.copy()
    df["has_promotion"] = 0
    for _, promo in promotions.iterrows():
        mask = (df[date_col] >= promo["start_date"]) & (df[date_col] <= promo["end_date"])
        df.loc[mask, "has_promotion"] = 1
    return df


def encode_categorical(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    """Label encode các cột categorical."""
    df = df.copy()
    for col in cols:
        df[col] = df[col].astype("category").cat.codes
    return df
