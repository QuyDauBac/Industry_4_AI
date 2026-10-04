"""Phân tích khi nào model sai (Ch.7): mẫu Fail bị bỏ sót, báo động giả,
và chuyện gì xảy ra khi điều kiện vận hành thay đổi (drift theo thời gian)."""


def missed_failures(y_true, proba, threshold: float):
    raise NotImplementedError


def false_alarms(y_true, proba, threshold: float):
    raise NotImplementedError
