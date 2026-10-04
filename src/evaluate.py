"""Đánh giá 3 mức. Đọc kết quả đã lưu trong results/ (viết sớm, thử trên LR).
Đường dẫn lấy từ config: oof_path, test_path, threshold_path, ablation_path, robustness_path.

Model level   : Precision / Recall / F1, ROC-AUC, PR-AUC, detection rate (= recall Fail),
                bootstrap khoảng tin cậy. Báo cáo số lượng cụ thể (vd 12/20) cạnh tỉ lệ %.
System level  : false alarm, latency (đo thời gian predict_proba trên 1 mẫu), robustness (đổi giai đoạn
                thời gian, thêm nhiễu, nhiều seed), computational cost.
Industrial    : tỉ lệ lỗi chặn được, lỗi lọt qua, khối lượng cảnh báo trên 1.000 lô;
                so với 3 mốc (không kiểm tra, kiểm tra ngẫu nhiên cùng số lượng, kiểm tra 100%);
                bảng capture@k. Không quy ra tiền. Ghi rõ SECOM không đo được downtime, năng lượng.
"""
import numpy as np


def model_level(y_true, proba, threshold: float) -> dict:
    raise NotImplementedError


def bootstrap_ci(y_true, proba, threshold: float, metric: str, n_boot: int = 1000, seed: int = 42):
    raise NotImplementedError


def system_level(model_name: str) -> dict:
    raise NotImplementedError


def industrial_level(y_true, proba, threshold: float, per: int = 1000) -> dict:
    raise NotImplementedError


def capture_at_k(y_true, proba, ks) -> "pd.DataFrame":
    raise NotImplementedError


def main() -> None:
    raise NotImplementedError


if __name__ == "__main__":
    main()
