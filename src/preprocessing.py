import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import STL


def summarize(df: pd.DataFrame, name: str = "", verbose: bool = True) -> pd.DataFrame:
    """Tóm tắt chất lượng dữ liệu: shape, dtype, null%, unique."""
    summary = pd.DataFrame({
        "dtype":    df.dtypes,
        "null_count":  df.isnull().sum(),
        "null_pct": (df.isnull().sum() / len(df) * 100).round(2),
        "unique":   df.nunique(),
        "sample":   df.iloc[0] if len(df) > 0 else None,
    })
    if verbose and name:
        print(f"\n=== {name} | shape: {df.shape} ===")
        print(summary.to_string())
    return summary


def drop_high_null_cols(df: pd.DataFrame, threshold: float = 0.5) -> pd.DataFrame:
    """Xóa các cột có tỉ lệ null vượt quá threshold (mặc định 50%)."""
    null_pct = df.isnull().sum() / len(df)
    cols_to_drop = null_pct[null_pct > threshold].index.tolist()
    if cols_to_drop:
        print(f"Dropping columns with >{threshold*100:.0f}% nulls: {cols_to_drop}")
    return df.drop(columns=cols_to_drop)


def fill_numeric_median(df: pd.DataFrame) -> pd.DataFrame:
    """Điền giá trị null của cột số bằng median."""
    num_cols = df.select_dtypes(include="number").columns
    df[num_cols] = df[num_cols].fillna(df[num_cols].median())
    return df


def fill_categorical_mode(df: pd.DataFrame) -> pd.DataFrame:
    """Điền giá trị null của cột categorical bằng mode."""
    cat_cols = df.select_dtypes(include="object").columns
    for col in cat_cols:
        df[col] = df[col].fillna(df[col].mode()[0])
    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Xóa các dòng trùng lặp."""
    before = len(df)
    df = df.drop_duplicates()
    removed = before - len(df)
    if removed > 0:
        print(f"Removed {removed} duplicate rows")
    return df


def parse_dates(df: pd.DataFrame, date_cols: list[str]) -> pd.DataFrame:
    """Chuyển các cột ngày tháng sang kiểu datetime."""
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    return df


def remove_outliers_iqr(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """Loại bỏ outliers theo phương pháp IQR (1.5x)."""
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    mask = (df[col] >= q1 - 1.5 * iqr) & (df[col] <= q3 + 1.5 * iqr)
    removed = (~mask).sum()
    if removed > 0:
        print(f"Removed {removed} outliers in column '{col}'")
    return df[mask]

def prepare_stl_dataframe(df_sales_cleaned):

    stl_df = (
        df_sales_cleaned[['date', 'revenue']]
        .drop_duplicates(subset='date')
        .sort_values('date')
    )

    stl_df['date'] = pd.to_datetime(
        stl_df['date']
    ).dt.normalize()

    stl_df = (
        stl_df
        .set_index('date')
        .asfreq('D')
    )

    if stl_df['revenue'].isna().sum() > 0:
        stl_df['revenue'] = (
            stl_df['revenue']
            .interpolate(method='time')
            .ffill()
            .bfill()
        )

    stl_df['LogRevenue'] = np.log1p(
        stl_df['revenue']
    )

    return stl_df