"""Chọn ngưỡng quyết định, dùng chung cho cả 3 model.

Quy tắc: chọn trên xác suất out-of-fold của tập TRAIN, không bao giờ chọn trên test.
Tiêu chí: tối đa F1, hoặc recall tối thiểu cho trước (không dùng hàm chi phí).
Có thể chọn theo ngân sách kiểm tra (số mẫu được đánh dấu tối đa).
"""
import json

import numpy as np

import config


def choose_threshold(y_true: np.ndarray, oof_proba: np.ndarray, method: str = "f1",
                     min_recall: float | None = None, max_flag_rate: float | None = None) -> float:
    """method: "f1" | "min_recall" | "budget". Trả về ngưỡng."""
    raise NotImplementedError


def save_threshold(model_name: str, threshold: float, method: str, **params) -> None:
    """Lưu ngưỡng vào config.threshold_path(model_name) để evaluate.py và dashboard dùng lại.

    Định dạng: {"model": ..., "method": "f1" | "min_recall" | "budget", "threshold": 0.37, ...tham số}
    """
    data = {"model": model_name, "method": method, "threshold": float(threshold), **params}
    path = config.threshold_path(model_name)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def load_threshold(model_name: str) -> float:
    """Đọc ngưỡng đã lưu của model."""
    data = json.loads(config.threshold_path(model_name).read_text(encoding="utf-8"))
    return float(data["threshold"])
