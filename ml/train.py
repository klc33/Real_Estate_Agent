import pandas as pd
from sklearn.model_selection import train_test_split

from ml.features import FEATURES, TARGET


# -------------------------
# LOAD DATA
# -------------------------

df = pd.read_csv("data/raw.csv")
df = df[FEATURES + [TARGET]]




# -------------------------
# SPLIT DATA (60/20/20)
# -------------------------

X = df[FEATURES]
y = df[TARGET]

# 60% train / 40% temp
X_train, X_temp, y_train, y_temp = train_test_split(
    X, y,
    test_size=0.4,
    random_state=42
)

# 20% val / 20% test
X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp,
    test_size=0.5,
    random_state=42
)

