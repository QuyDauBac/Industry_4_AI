"""Logistic Regression (baseline).

- class_weight="balanced" để xử lý mất cân bằng lớp
- Nhạy với scaling và feature selection -> đặt sau preprocessor trong cùng Pipeline
"""
from sklearn.linear_model import LogisticRegression

import config

PARAM_GRID = {
    f"{config.STEP_MODEL}__C": [0.01, 0.1, 1, 10],
}


def build_model(class_weight: str | None = "balanced") -> LogisticRegression:
    raise NotImplementedError


def run_ablation() -> dict:
    """Ablation LR: có/không class_weight, ngưỡng 0.5 vs đã chọn, có/không feature selection.
    Lưu kết quả vào config.ablation_path("lr") (định dạng: xem README) để notebook so sánh tổng hợp."""
    raise NotImplementedError
