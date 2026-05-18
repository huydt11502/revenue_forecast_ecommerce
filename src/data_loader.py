import pandas as pd
from pathlib import Path

RAW = Path(__file__).parent.parent / "data" / "raw"
PROCESSED = Path(__file__).parent.parent / "data" / "processed"


def load_raw(group: str, filename: str) -> pd.DataFrame:
    """Load a raw CSV file by group (master/transaction/analytical/operational)."""
    path = RAW / group / filename
    return pd.read_csv(path, low_memory=False)


def load_all_raw() -> dict[str, pd.DataFrame]:
    """Load tất cả 15 bảng dữ liệu gốc, trả về dict {tên_bảng: DataFrame}."""
    tables = {
        # Master
        "products":    load_raw("master", "products.csv"),
        "customers":   load_raw("master", "customers.csv"),
        "promotions":  load_raw("master", "promotions.csv"),
        "geography":   load_raw("master", "geography.csv"),
        # Transaction
        "orders":      load_raw("transaction", "orders.csv"),
        "order_items": load_raw("transaction", "order_items.csv"),
        "payments":    load_raw("transaction", "payments.csv"),
        "shipments":   load_raw("transaction", "shipments.csv"),
        "returns":     load_raw("transaction", "returns.csv"),
        "reviews":     load_raw("transaction", "reviews.csv"),
        # Analytical
        "sales":       load_raw("analytical", "sales.csv"),
        # Operational
        "inventory":   load_raw("operational", "inventory.csv"),
        "web_traffic": load_raw("operational", "web_traffic.csv"),
    }
    return tables


def load_processed(filename: str, subfolder: str = "cleaned") -> pd.DataFrame:
    """Load một file đã xử lý từ data/processed/."""
    return pd.read_csv(PROCESSED / subfolder / filename)


def save_processed(df: pd.DataFrame, filename: str, subfolder: str = "cleaned") -> None:
    """Lưu DataFrame vào data/processed/."""
    path = PROCESSED / subfolder / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Saved: {path}")
