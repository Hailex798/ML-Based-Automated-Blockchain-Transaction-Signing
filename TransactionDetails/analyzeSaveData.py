import json
import csv

def save_to_csv(json_file="fetched_data.json", csv_file="transactions.csv"):
    with open(json_file, "r") as file:
        transactions = json.load(file)
    
    keys = transactions[0].keys()
    with open(csv_file, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()
        writer.writerows(transactions)
    
    print(f"Data saved to {csv_file}")

# Usage
if __name__ == "__main__":
    save_to_csv()
