import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# -----------------------------
# Load Data
# -----------------------------
df = pd.read_csv("ecommerce_returns_synthetic_data.csv")

# Target Encoding
df["Return_Status"] = df["Return_Status"].map({
    "Returned": 1,
    "Not Returned": 0
})

# Drop columns not useful for prediction
df = df.drop(columns=[
    "Order_ID",
    "Product_ID",
    "User_ID",
    "Return_Date",
    "Return_Reason"
])

# Handle missing values
df["Days_to_Return"] = df["Days_to_Return"].fillna(0)

# Features / Target
X = df.drop("Return_Status", axis=1)
y = df["Return_Status"]

# Categorical & Numerical Columns
categorical_cols = [
    "Product_Category",
    "User_Gender",
    "User_Location",
    "Payment_Method",
    "Shipping_Method"
]

numerical_cols = [
    "Product_Price",
    "Order_Quantity",
    "Days_to_Return",
    "User_Age",
    "Discount_Applied"
]

# Preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
        ("num", "passthrough", numerical_cols)
    ]
)

# Model
model = RandomForestClassifier(
    n_estimators=300,
    max_depth=12,
    random_state=42,
    class_weight="balanced"
)

pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("model", model)
])

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Train
pipeline.fit(X_train, y_train)

# Evaluate
y_pred = pipeline.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"Accuracy: {accuracy:.2f}")
print(classification_report(y_test, y_pred))

# Save Model
joblib.dump(pipeline, "refund_model.pkl")

print("Model saved as refund_model.pkl")
