"""
Preprocessing pipeline for the Ames Housing dataset.
"""

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

from ml.features import NUM_FEATURES, CAT_FEATURES


# Numeric pipeline: impute with median, then scale
numeric_pipeline = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])


# Categorical pipeline: impute with most frequent, then one-hot encode
categorical_pipeline = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="constant", fill_value="missing")),
    ("encoder", OneHotEncoder(
        handle_unknown="ignore", 
        sparse_output=False,
        drop="first"  # Avoid multicollinearity
    ))
])


# Full preprocessor combining both pipelines
preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_pipeline, NUM_FEATURES),
        ("cat", categorical_pipeline, CAT_FEATURES),
    ],
    remainder="drop",  # Drop any columns not specified
    verbose_feature_names_out=False  # Cleaner feature names
)