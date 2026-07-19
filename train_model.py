import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("data/hydro_power.csv")

# Display first 5 rows
print(df.head())

# Dataset information
print("\nDataset Shape:", df.shape)
print("\nColumn Names:")
print(df.columns)

# Missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Dataset Summary
print("\nDataset Summary:")
print(df.describe())

# Data Types
print("\nData Types:")
print(df.dtypes)

# Correlation Matrix
print("\nCorrelation:")
print(df.corr(numeric_only=True))

# Correlation Heatmap
plt.figure(figsize=(10,8))
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="Blues")
plt.title("Correlation Heatmap")
plt.show()

# Target Distribution
plt.figure(figsize=(8,5))
sns.histplot(df["Power Generation (MW)"], bins=30, kde=True)
plt.title("Power Generation Distribution")
plt.show()

from sklearn.model_selection import train_test_split

# Convert Date to datetime
df["Date"] = pd.to_datetime(df["Date"])

# Create new features
df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month
df["Day"] = df["Date"].dt.day

# Drop Date column
df = df.drop("Date", axis=1)

# Features and Target
X = df.drop("Power Generation (MW)", axis=1)
y = df["Power Generation (MW)"]

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

print("Training Data:", X_train.shape)
print("Testing Data:", X_test.shape)

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Train Model
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# Prediction
y_pred = model.predict(X_test)

# Evaluation
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = mse ** 0.5
r2 = r2_score(y_test, y_pred)

print("\nModel Performance")
print("MAE :", mae)
print("RMSE:", rmse)
print("R2 Score:", r2)

import joblib

joblib.dump(model, "hydro_power_model.pkl")

print("Model saved successfully!")