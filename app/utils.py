def get_missing_features(features: dict):
    return [k for k, v in features.items() if v is None]