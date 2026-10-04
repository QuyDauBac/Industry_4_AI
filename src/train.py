"""Runner chung. Các file khác (evaluate, explain, dashboard) phụ thuộc file này -> giao bản thô sớm.

Chạy (từ thư mục gốc của repo):
    python -m src.train --model lr|rf|xgb                      huấn luyện + chọn ngưỡng
    python -m src.train --model lr --threshold-method f1       f1 (mặc định) | min_recall | budget
    python -m src.train --model lr --ablation                  chạy ablation (gọi run_ablation của model)
    python -m src.train --model lr --time-block K              robustness: train/test ở giai đoạn khác

Chạy thường tạo ra 4 file. Đường dẫn LẤY TỪ config, không tự ghép chuỗi:
- config.oof_path(model)        results/oof_proba/<model>.npy    P(Fail) out-of-fold trên train (5-fold stratified)
- config.test_path(model)       results/test_proba/<model>.npy   P(Fail) trên test
- config.threshold_path(model)  results/threshold_<model>.json   ngưỡng chọn trên oof (threshold.save_threshold)
- config.model_path(model)      saved_models/<model>.joblib      pipeline huấn luyện trên toàn bộ train (không commit)
--ablation ghi config.ablation_path(model); --time-block ghi config.robustness_path(model).
Định dạng JSON của ablation / robustness: xem README, mục "File đầu ra dùng chung".

Pipeline đầy đủ = build_preprocessor() + 1 bước model cuối (tên config.STEP_MODEL).
Mọi nơi (train, explain, dashboard) lấy pipeline từ build_pipeline(), không tự lắp ráp.

Ghi chú mở rộng: nếu sau này thêm chế độ stratified CV lặp lại để đối chiếu, ngưỡng và hyperparameter
phải chọn BÊN TRONG từng fold train (nested), nếu không kết quả đối chiếu bị lạc quan.
"""
from imblearn.pipeline import Pipeline

import config
from src.models import logistic, random_forest, xgboost_model
from src.preprocess import build_preprocessor


def build_pipeline(name: str, y_train=None, k_features: int | None = config.K_FEATURES) -> Pipeline:
    """Ghép tiền xử lý + model thành 1 Pipeline chưa fit.

    - Các bước tiền xử lý giữ tên trong config.PREP_STEPS; bước cuối tên config.STEP_MODEL.
    - y_train chỉ cần cho "xgb": scale_pos_weight = n_pass / n_fail (tính trên train).
    - k_features=None bỏ bước chọn đặc trưng (dùng cho ablation).
    """
    prep = build_preprocessor(k_features)
    if name == "lr":
        model = logistic.build_model()
    elif name == "rf":
        model = random_forest.build_model()
    elif name == "xgb":
        spw = None
        if y_train is not None:
            spw = float((y_train == config.PASS).sum() / (y_train == config.FAIL).sum())
        model = xgboost_model.build_model(scale_pos_weight=spw)
    else:
        raise ValueError(f"model khong hop le: {name}. Chon mot trong {config.MODEL_NAMES}")
    return Pipeline(list(prep.steps) + [(config.STEP_MODEL, model)])


def train_model(name: str, time_block=None):
    raise NotImplementedError


def main() -> None:
    raise NotImplementedError


if __name__ == "__main__":
    main()
