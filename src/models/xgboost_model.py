"""XGBoost. Xử lý imbalance bằng scale_pos_weight = n_pass / n_fail (tính trên train)."""
from xgboost import XGBClassifier

import config

PARAM_GRID = {}


def build_model(scale_pos_weight: float | None = None) -> XGBClassifier:
    raise NotImplementedError


def run_ablation() -> dict:
    """Lưu vào config.ablation_path("xgb")."""
    raise NotImplementedError
