"""Chia dữ liệu.

Quy ước: 80/20 theo thời gian (cắt theo số dòng), in số mẫu / số lỗi / tỉ lệ lỗi từng phần.
Có thêm chế độ stratified để đối chiếu. Không cân bằng lại tập test.
"""
import pandas as pd

import config


def time_split(X: pd.DataFrame, y: pd.Series, timestamps: pd.Series, test_size: float = config.TEST_SIZE):
    """Sắp xếp theo timestamp, cắt theo số dòng. Trả về X_train, X_test, y_train, y_test."""
    raise NotImplementedError


def stratified_split(X: pd.DataFrame, y: pd.Series, test_size: float = config.TEST_SIZE, seed: int = config.SEED):
    """Chia ngẫu nhiên có stratify - chỉ dùng để đối chiếu với chia theo thời gian."""
    raise NotImplementedError


def describe_split(y_train: pd.Series, y_test: pd.Series) -> pd.DataFrame:
    """Bảng số mẫu / số Fail / tỉ lệ Fail của train và test (in ra và đưa vào báo cáo)."""
    raise NotImplementedError
