import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Define the paths
input_csv_path = r"D:\New folder\ML-Based-Automated-Blockchain-Transaction-Signing-main\TransactionDetails\transactions.csv"
output_cleaned_csv_path = r"D:\New folder\ML-Based-Automated-Blockchain-Transaction-Signing-main\TransactionDetails\transactions_cleaned.csv"
model_path = r"D:\New folder\ML-Based-Automated-Blockchain-Transaction-Signing-main\Model_traning\model.pkl"

# Load the CSV file
try:
    data = pd.read_csv(input_csv_path)
    print("CSV file loaded successfully!")
except FileNotFoundError:
    print(f"Error: The file at {input_csv_path} was not found. Please check the file path.")
    exit()

# View initial dataset info
print("\nInitial Dataset Info:")
print(data.info())

# Check for missing values
print("\nMissing Values in Dataset:")
print(data.isnull().sum())

# Separate numeric and non-numeric columns
numeric_cols = data.select_dtypes(include=['number']).columns
non_numeric_cols = data.select_dtypes(exclude=['number']).columns

# Handle missing values
# Numeric: Fill with mean
data[numeric_cols] = data[numeric_cols].fillna(data[numeric_cols].mean())

# Non-numeric: Fill with mode
for col in non_numeric_cols:
    data[col] = data[col].fillna(data[col].mode()[0])

# Verify missing values are handled
print("\nMissing Values After Imputation:")
print(data.isnull().sum())

# Save the cleaned data
data.to_csv(output_cleaned_csv_path, index=False)
print(f"Cleaned data saved to {output_cleaned_csv_path}")

# Check if the target column exists
target_column = 'target'
if target_column not in data.columns:
    print(f"Error: Target column '{target_column}' not found in the dataset. Add the target column to proceed.")
    exit()

# Split the data into features (X) and target (y)
X = data.drop(columns=[target_column])
y = data[target_column]

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize numeric features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Train a Random Forest model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.2f}")

# Save the trained model
joblib.dump(model, model_path)
print(f"Trained model saved to {model_path}")






import joblib
import numpy as np

# Model ko load karna
model = joblib.load(r"D:\New folder\ML-Based-Automated-Blockchain-Transaction-Signing-main\Model_traning\model.pkl")

# Naye data ka example
new_data = np.array([[feature1_value, feature2_value, feature3_value, ...]])  # Feature values replace karein

# Prediction karna
prediction = model.predict(new_data)
print(f"Prediction: {prediction}")






