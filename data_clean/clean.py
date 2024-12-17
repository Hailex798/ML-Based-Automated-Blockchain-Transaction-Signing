import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Load the dataset
df = pd.read_csv("E:/ML-Blockchain-DS/TransactionDetails/transactions.csv")


# Display initial dataset information
print("Initial Dataset Information:")
print(df.info())
print("\nPreview of the dataset:")
print(df.head())

# Select relevant columns for cleaning
columns_to_keep = ['from', 'to', 'value', 'gas', 'gasPrice', 'nonce', 'input','isError']
df = df[columns_to_keep]

print("\nDataset after selecting relevant columns:")
print(df.head())

# Convert `value`, `gas`, `gasPrice`, and `nonce` to numeric
numerical_columns = ['value', 'gas', 'gasPrice', 'nonce']
for col in numerical_columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Fill missing numerical values with the median
df[numerical_columns] = df[numerical_columns].fillna(df[numerical_columns].median())

# Normalize numerical columns using MinMaxScaler
scaler = MinMaxScaler()
df[numerical_columns] = scaler.fit_transform(df[numerical_columns])

print("\nDataset after normalization:")
print(df.head())

# Save the cleaned data
df.to_csv("cleaned_transactions.csv", index=False)
print("\nCleaned dataset saved to 'cleaned_transactions.csv'")
