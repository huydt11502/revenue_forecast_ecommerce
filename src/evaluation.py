import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from pathlib import Path

FIGURES_DIR = Path(__file__).parent.parent / "outputs" / "figures" / "model"


def evaluate(y_true, y_pred, label: str = "Model") -> dict:
    """Tính MAE, RMSE, R² và in kết quả."""
    mae  = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2   = r2_score(y_true, y_pred)

    print(f"\n{'='*40}")
    print(f" {label}")
    print(f"{'='*40}")
    print(f"  MAE  : {mae:,.2f}")
    print(f"  RMSE : {rmse:,.2f}")
    print(f"  R²   : {r2:.4f}")
    print(f"{'='*40}\n")

    return {"label": label, "MAE": mae, "RMSE": rmse, "R2": r2}


def plot_predictions(y_true, y_pred, dates=None, label: str = "Model", save: bool = True):
    """Vẽ biểu đồ so sánh giá trị thực tế vs dự báo."""
    fig, axes = plt.subplots(2, 1, figsize=(14, 8))

    x = dates if dates is not None else range(len(y_true))

    # Actual vs Predicted
    axes[0].plot(x, y_true, label="Actual", color="steelblue", linewidth=1.5)
    axes[0].plot(x, y_pred, label="Predicted", color="tomato", linestyle="--", linewidth=1.5)
    axes[0].set_title(f"{label} — Actual vs Predicted Revenue")
    axes[0].set_ylabel("Revenue")
    axes[0].legend()
    axes[0].grid(alpha=0.3)

    # Residuals
    residuals = np.array(y_true) - np.array(y_pred)
    axes[1].bar(x, residuals, color="gray", alpha=0.6)
    axes[1].axhline(0, color="black", linewidth=1)
    axes[1].set_title("Residuals (Actual - Predicted)")
    axes[1].set_ylabel("Error")
    axes[1].grid(alpha=0.3)

    plt.tight_layout()

    if save:
        FIGURES_DIR.mkdir(parents=True, exist_ok=True)
        path = FIGURES_DIR / f"{label.lower().replace(' ', '_')}_predictions.png"
        plt.savefig(path, dpi=150, bbox_inches="tight")
        print(f"Figure saved: {path}")

    plt.show()


def compare_models(results: list[dict]) -> pd.DataFrame:
    """So sánh nhiều mô hình từ list kết quả evaluate()."""
    df = pd.DataFrame(results).set_index("label")
    print(df.to_string())

    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    for ax, metric in zip(axes, ["MAE", "RMSE", "R2"]):
        df[metric].plot(kind="bar", ax=ax, color="steelblue", edgecolor="black")
        ax.set_title(metric)
        ax.set_xlabel("")
        ax.tick_params(axis="x", rotation=30)
        ax.grid(axis="y", alpha=0.3)

    plt.suptitle("Model Comparison", fontsize=13, fontweight="bold")
    plt.tight_layout()

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    plt.savefig(FIGURES_DIR / "model_comparison.png", dpi=150, bbox_inches="tight")
    plt.show()

    return df
