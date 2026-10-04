"""Giải thích model (Ch.7): hệ số LR, importance RF, SHAP cho XGBoost.

XGBoost: dùng giá trị SHAP có sẵn của XGBoost, không cần cài thêm thư viện shap:
    booster.predict(xgboost.DMatrix(X_đã_tiền_xử_lý), pred_contribs=True)   # cột cuối là bias
Lấy các bước từ pipeline.named_steps (tên bước: config.PREP_STEPS, config.STEP_MODEL).

Lưu ý khi viết báo cáo: đây là mức độ đóng góp của sensor vào cảnh báo, không phải quan hệ nhân quả.
Chỉ số cột phải được map về cột gốc trong 590 cột, không phải chỉ số sau khi lọc.
"""


def lr_coefficients(pipeline):
    raise NotImplementedError


def rf_importance(pipeline):
    raise NotImplementedError


def xgb_shap(pipeline, X):
    raise NotImplementedError
