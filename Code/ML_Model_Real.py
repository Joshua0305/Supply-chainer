import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import os

# --- 1. Load Real Historical Dataset ---
print("--- Loading Real Historical Data ---")
df = pd.read_csv('Execution/Supplychainer_Real_Historical_Dataset.csv')

# --- 2. Categorical Encoding ---
print("--- Categorical Encoding ---")
le_dict = {}
categorical_cols = ['Leg_Type', 'Origin_Node', 'Destination_Node', 'Transport_Mode', 'Condition_Flag']

for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col].astype(str))
    le_dict[col] = le

# --- 3. Split Data ---
X = df.drop(['Delay_Hours'], axis=1)
y = df['Delay_Hours']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- 4. Train Quantile Model (alpha=0.85) ---
print("--- Training Supplychainer p85 Real-Data Brain ---")
model = GradientBoostingRegressor(
    loss='quantile',
    alpha=0.85,          
    n_estimators=400,    
    learning_rate=0.05,
    max_depth=6,         
    random_state=42
)

model.fit(X_train, y_train)
print("SUCCESS: Real-Data Quantile Model trained.")

# --- 5. Export to Production ---
if not os.path.exists('Execution'):
    os.makedirs('Execution')

joblib.dump(model, 'Execution/risk_model.pkl')
joblib.dump(le_dict, 'Execution/label_encoders.pkl')
print("Production artifacts updated: Execution/risk_model.pkl")
