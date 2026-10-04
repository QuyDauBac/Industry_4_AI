"""Load dữ liệu SECOM.

Cần làm:
- Đọc secom.data (sep=r"\\s+", header=None): kỳ vọng (1567, 590).
- Đọc secom_labels.data: cột 0 = nhãn (-1/1), cột 1 = timestamp (dd/mm/YYYY HH:MM:SS).
- Đổi nhãn sang 0 = Pass, 1 = Fail (config.LABEL_MAP).
- Giữ nguyên thứ tự theo thời gian (sắp xếp theo timestamp nếu cần).
"""
import pandas as pd

import config


def load_data() -> tuple[pd.DataFrame, pd.Series, pd.Series]:
    """Trả về (X, y, timestamps).

    X: DataFrame (n_mẫu, 590), cột đánh số 0..589
    y: Series 0/1 (1 = Fail)
    timestamps: Series datetime cùng index với X, đã sắp xếp tăng dần
    """
    raise NotImplementedError


def validate_structure() -> None:
    """Kiểm tra số trường mỗi dòng của secom.data (kỳ vọng đều = 590) và in kết quả."""
    raise NotImplementedError
