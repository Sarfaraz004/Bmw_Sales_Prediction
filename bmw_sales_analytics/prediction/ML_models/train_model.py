import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import os

# Path to dataset
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(BASE_DIR, 'data.csv')

# Load dataset
df = pd.read_csv(data_path)

print("✅ Data loaded successfully")
print("Shape:", df.shape)
print("Columns:", df.columns.tolist())

# Drop any missing values (optional, but keeps model clean)
df.dropna(inplace=True)

# Features (X) and target (y)
X = df.drop(['Sales_Volume', 'Sales_Classification'], axis=1)
y = df['Sales_Volume']

# Encode categorical columns
categorical_cols = X.select_dtypes(include=['object']).columns

label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col])
    label_encoders[col] = le

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestRegressor(
    n_estimators=200,
    random_state=42,
    n_jobs=-1
)
model.fit(X_train, y_train)

# Predict and evaluate
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"✅ Model trained successfully!")
print(f"MAE: {mae:.2f}")
print(f"R² Score: {r2:.2f}")

# Save model & encoders
model_path = os.path.join(BASE_DIR, 'trained_model.pkl')
encoders_path = os.path.join(BASE_DIR, 'encoders.pkl')

joblib.dump(model, model_path)
joblib.dump(label_encoders, encoders_path)

print(f"✅ Model saved at: {model_path}")
print(f"✅ Encoders saved at: {encoders_path}")
