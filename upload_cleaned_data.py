import csv
import time
import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase Admin SDK
cred = credentials.Certificate("C:/Users/PMLS/Downloads/realtime-home-monitoring-firebase-adminsdk-y7zjb-96c7216133.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://realtime-home-monitoring-default-rtdb.firebaseio.com"  # Corrected Firebase database URL
})

# Function to upload data from CSV to Firebase with a delay between sending all rows
def upload_csv_to_firebase_with_delay(csv_file_path, database_path, num_rows=50, delay_seconds=5):
    ref = db.reference(database_path)  # Reference to the database path
    rows = []

    # Read the CSV file and store the rows
    with open(csv_file_path, "r") as file:
        reader = csv.DictReader(file)
        for index, row in enumerate(reader):
            if index >= num_rows:  # Limit to the first num_rows
                break
            rows.append(row)  # Collect rows in a list

    # Upload all rows to Firebase with a delay between each
    for index, row in enumerate(rows):
        key = f"item_{index}"  # Create a unique key for each entry
        try:
            ref.child(key).set(row)  # Upload each row to Firebase
            print(f"Uploaded: {row}")
        except Exception as e:
            print(f"Failed to upload row {index}: {e}")

        # Wait for the specified delay time before uploading the next row
        if index < len(rows) - 1:  # Avoid delay after the last row
            print(f"Waiting for {delay_seconds} seconds before uploading the next row...")
            time.sleep(delay_seconds)

# Path to your cleaned CSV file and Firebase database node
csv_file_path = "C:/Users/PMLS/Desktop/cleaned_data.csv"  # Replace with your absolute CSV file path
database_path = "iot_data_stream"  # Replace with the node where you want to upload

# Call the function to upload 50 rows with a delay of 5 seconds
upload_csv_to_firebase_with_delay(csv_file_path, database_path, num_rows=50, delay_seconds=5)
