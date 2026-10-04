"""Random Forest. Xử lý imbalance bằng class_weight."""
from sklearn.ensemble import RandomForestClassifier

import config

PARAM_GRID = {}


def build_model(class_weight: str | None = "balanced_subsample") -> RandomForestClassifier:
    raise NotImplementedError


def run_ablation() -> dict:
    """Lưu vào config.ablation_path("rf")."""
    raise NotImplementedError
