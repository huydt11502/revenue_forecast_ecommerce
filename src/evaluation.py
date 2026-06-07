import numpy as np

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

def evaluate(y_true, y_pred, n_features, label: str = "Model"):
    """Tính MAE, RMSE, R² và Adjusted R²."""

    mae  = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2   = r2_score(y_true, y_pred)

    # Adjusted R²
    n = len(y_true)
    adj_r2 = 1 - ((1 - r2) * (n - 1) / (n - n_features - 1))

    print(f"\n{'='*40}")
    print(f" {label}")
    print(f"{'='*40}")
    print(f"  MAE            : {mae:.4f}")
    print(f"  RMSE           : {rmse:.4f}")
    print(f"  R²             : {r2:.4f}")
    print(f"  Adjusted R²    : {adj_r2:.4f}")
    print(f"{'='*40}\n")

    return {
        "label": label,
        "MAE": round(mae, 4),
        "RMSE": round(rmse, 4),
        "R2": round(r2, 4),
        "Adjusted_R2": round(adj_r2, 4)
    }