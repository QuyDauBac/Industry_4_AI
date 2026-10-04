"""Pipeline tiền xử lý. Mọi bước chỉ fit trên train.

Các bước dự kiến (tên bước lấy từ config.PREP_STEPS; giải thích lý do từng bước trong báo cáo Ch.4):
1. "missing"  : MissingRateSelector - bỏ cột thiếu > config.MISSING_THRESHOLD
2. "impute"   : SimpleImputer(median, add_indicator=config.ADD_MISSING_INDICATOR)
                Đây cũng là bước FEATURE ENGINEERING: thêm cột đánh dấu "giá trị này bị thiếu"
                (thiếu dữ liệu cảm biến có thể là tín hiệu). Nếu đặt ADD_MISSING_INDICATOR=False thì
                báo cáo phải ghi rõ lý do không tạo đặc trưng mới (590 cột đã ẩn danh).
3. "variance" : VarianceThreshold - bỏ cột hằng số
4. "outlier"  : (tùy chọn) xử lý ngoại lệ; không dùng thì bỏ bước này
5. "scale"    : StandardScaler
6. "select"   : SelectKBest(f_classif, k=config.K_FEATURES)

Imbalance: xử lý bằng class_weight / scale_pos_weight trong từng model. Nếu vẫn dùng resampling
(imblearn) thì thêm thành MỘT BƯỚC RIÊNG ở cuối danh sách bước, ngay trước bước model - không lồng
Pipeline trong Pipeline (src.train.build_pipeline ghép bằng cách nối các bước lại).
Chỉ số cột sau khi lọc/thêm phải truy ngược được về cột gốc: MissingRateSelector cần có get_support().

LƯU Ý: lớp MissingRateSelector được định nghĩa ở DUY NHẤT file này. File .joblib ghi nhớ
đường dẫn module của lớp, nên không đổi tên/chuyển file sau khi đã lưu pipeline.
"""
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline

import config


class MissingRateSelector(BaseEstimator, TransformerMixin):
    """Bỏ các cột có tỉ lệ thiếu vượt ngưỡng (tham khảo secom_preprocessing.py của thầy)."""

    def __init__(self, threshold: float = config.MISSING_THRESHOLD):
        self.threshold = threshold

    def fit(self, X, y=None):
        raise NotImplementedError

    def transform(self, X):
        raise NotImplementedError

    def get_support(self):
        """Mask boolean các cột được giữ (explain.py dùng để truy ngược về cột gốc)."""
        raise NotImplementedError


def build_preprocessor(k_features: int | None = config.K_FEATURES) -> Pipeline:
    """Trả về Pipeline tiền xử lý chưa fit (các bước đặt tên theo config.PREP_STEPS).

    Chỉ gồm tiền xử lý, KHÔNG gồm model: model được nối thêm ở src.train.build_pipeline().
    k_features=None để bỏ bước "select" (ablation).
    """
    raise NotImplementedError
