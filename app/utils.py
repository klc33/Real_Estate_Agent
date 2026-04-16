from typing import Dict, List, Any


def get_missing_features(features: Dict[str, Any]) -> List[str]:
    """
    Identify which expected features are missing or None.
    Excludes metadata fields like 'completeness'.
    """
    if not features:
        return []
    
    missing = []
    for key, value in features.items():
        # Skip metadata fields
        if key in ["completeness"]:
            continue
        # Check if value is None or missing
        if value is None:
            missing.append(key)
    
    return missing


def calculate_completeness_score(features: Dict[str, Any]) -> float:
    """
    Calculate what percentage of features are present.
    """
    total = 0
    present = 0
    
    for key, value in features.items():
        if key == "completeness":
            continue
        total += 1
        if value is not None:
            present += 1
    
    if total == 0:
        return 0.0
    
    return present / total


def validate_features(features: Dict[str, Any]) -> tuple[bool, List[str]]:
    """
    Validate feature values are within reasonable ranges.
    Returns (is_valid, list_of_issues)
    """
    issues = []
    
    # Numeric range validations
    if features.get("LotArea") is not None:
        if features["LotArea"] <= 0:
            issues.append("LotArea must be positive")
        elif features["LotArea"] > 500000:
            issues.append("LotArea seems unusually large")
    
    if features.get("OverallQual") is not None:
        if not 1 <= features["OverallQual"] <= 10:
            issues.append("OverallQual must be between 1 and 10")
    
    if features.get("YearBuilt") is not None:
        if features["YearBuilt"] < 1800:
            issues.append("YearBuilt seems too early")
        elif features["YearBuilt"] > 2025:
            issues.append("YearBuilt cannot be in the future")
    
    if features.get("GrLivArea") is not None:
        if features["GrLivArea"] <= 0:
            issues.append("GrLivArea must be positive")
        elif features["GrLivArea"] > 20000:
            issues.append("GrLivArea seems unusually large")
    
    if features.get("BedroomAbvGr") is not None:
        if features["BedroomAbvGr"] < 0:
            issues.append("BedroomAbvGr cannot be negative")
        elif features["BedroomAbvGr"] > 20:
            issues.append("BedroomAbvGr seems unusually high")
    
    return len(issues) == 0, issues