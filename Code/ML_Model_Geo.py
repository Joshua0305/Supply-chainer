import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import os

# --- 1. Load Geographic Dataset ---
print("--- Loading Geographic Data ---")
df = pd.read_csv('Supplychainer_Geographic_Dataset.csv')

# --- 2. Categorical Encoding (True Geographic Intelligence) ---
print("--- Categorical Encoding (Geographic Nodes) ---")
le_dict = {}
categorical_cols = ['Leg_Type', 'Origin_Node', 'Destination_Node', 'Transport_Mode', 'Condition_Flag']

for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col].astype(str))
    le_dict[col] = le
    print(f"  Encoded {col}: {len(le.classes_)} unique classes")

# --- 3. Split Data ---
X = df.drop(['Delay_Hours'], axis=1)
y = df['Delay_Hours']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"--- Training on {X_train.shape[0]} scenarios ---")

# --- 4. Train Quantile Model (alpha=0.85) ---
# Goal: Predict the 85th percentile worst-case delay
print("--- Training Supplychainer p85 Quantile Brain ---")
model = GradientBoostingRegressor(
    loss='quantile',
    alpha=0.85,          
    n_estimators=300,    # Increased for better node-specific learning
    learning_rate=0.05,
    max_depth=5,         
    random_state=42
)

model.fit(X_train, y_train)
print("Quantile Model successfully trained on Real Geographic Data!")

# --- 5. Evaluate ---
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"Model Performance: MAE={mae:.2f}h, R2={r2:.4f}")

# --- 6. Export to Production ---
# We overwrite the Execution artifacts to eliminate the Pharma Shim
print("--- Exporting New Production Artifacts ---")
if not os.path.exists('Execution'):
    os.makedirs('Execution')

joblib.dump(model, 'Execution/risk_model.pkl')
joblib.dump(le_dict, 'Execution/label_encoders.pkl')

print("SUCCESS: risk_model.pkl and label_encoders.pkl updated with Geographic Node intelligence.")
