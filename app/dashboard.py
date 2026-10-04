"""Dashboard Streamlit (mô phỏng chạy trên máy cá nhân: Data -> AI -> Decision).

Chạy: streamlit run app/dashboard.py

Hiển thị: trạng thái lô/mẫu hiện tại (SECOM không có mã máy), risk score P(Fail), cảnh báo,
khuyến nghị hành động, nút kỹ sư xác nhận (human-in-the-loop).

Đầu vào: pipeline đã huấn luyện của model tốt nhất (config.model_path), ngưỡng của model đó
(threshold.load_threshold), và các mẫu của tập test để "phát lại" như dữ liệu đang đến.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import config  # noqa: E402


def predict_risk(pipeline, sample) -> float:
    """Trả về P(Fail) của một mẫu (DataFrame 1 dòng, đủ 590 cột gốc)."""
    return float(pipeline.predict_proba(sample)[0, config.FAIL])


def recommend_action(risk: float, threshold: float) -> str:
    """Từ risk score và ngưỡng đã chọn trả về khuyến nghị hành động
    (ví dụ "Giữ lô, kiểm tra thêm" / "Cho qua"). Kỹ sư xác nhận hoặc bác bỏ khuyến nghị này."""
    raise NotImplementedError


def main() -> None:
    """Dựng giao diện Streamlit."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
