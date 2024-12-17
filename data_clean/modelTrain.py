import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib

# Load the cleaned dataset
data_path = "cleaned_transactions.csv"  # Update the path if needed
df = pd.read_csv(data_path)

# Check the structure of the dataset
print("Cleaned Data Information:")
print(df.info())
print("\nPreview of the cleaned data:")
print(df.head())

# Ensure the target column 'isError' exists
if 'isError' not in df.columns:
    raise ValueError("The 'isError' column is missing from the dataset. Please ensure the cleaned data includes it.")

# Define the target variable and features
target = 'isError'
features = ['value', 'gas', 'gasPrice', 'nonce']  # Add more numeric features as needed

# Separate features and target
X = df[features]
y = df[target]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the model
print("\nTraining the Random Forest model...")
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
print("\nModel Evaluation:")
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print("\nClassification Report:")
print(classification_report(y_test, y_pred))
print("\nAccuracy Score:")
print(accuracy_score(y_test, y_pred))

# Save the trained model
model_save_path = "random_forest_model.pkl"
joblib.dump(model, model_save_path)
print(f"\nModel saved to {model_save_path}")

# Load the saved model and make predictions
print("\nLoading the saved model...")
loaded_model = joblib.load(model_save_path)
print("Model loaded successfully!")

# Example test data for predictions (replace with your actual data)
test_data = pd.DataFrame({
    'value': [1.2, 0.5, 2.3],
    'gas': [21000, 50000, 30000],
    'gasPrice': [200, 150, 180],
    'nonce': [0.0, 0.1, 0.2]
})

# Make predictions using the loaded model
predictions = loaded_model.predict(test_data)
print("Predictions:", predictions)

# Optional: Check feature importances of the model
print("Feature Importances:", loaded_model.feature_importances_)
