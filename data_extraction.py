import requests
import json
from datetime import datetime
import boto3

API_KEY = "b03769ccccd4da9e77d5f61bbd6edb1e"

url = f"http://api.aviationstack.com/v1/flights?access_key={API_KEY}"

response = requests.get(url)

api_data = response.json()

# Extract only data records
flights = api_data["data"]

# Flatten records
cleaned_data = []

for flight in flights:
    cleaned_record = {
        "flight_date": flight.get("flight_date"),
        "flight_status": flight.get("flight_status"),

        "departure_airport": flight.get("departure", {}).get("airport"),
        "departure_scheduled": flight.get("departure", {}).get("scheduled"),

        "arrival_airport": flight.get("arrival", {}).get("airport"),
        "arrival_scheduled": flight.get("arrival", {}).get("scheduled"),

        "airline": flight.get("airline", {}).get("name"),

        "flight_number": flight.get("flight", {}).get("number")
    }

    cleaned_data.append(cleaned_record)

# Save as NDJSON
filename = "flight_data.json"

with open(filename, "w") as f:
    for record in cleaned_data:
        f.write(json.dumps(record) + "\n")

# Upload to S3
s3 = boto3.client('s3')

bucket_name = 'aviataion-project'

current_time = datetime.now()

timestamp = current_time.strftime("%Y%m%d_%H%M%S")

s3_key = f"raw_layer/{current_time.year}-{current_time.month:02}-{current_time.day:02}/flight_data_{timestamp}.json"

s3.upload_file(filename, bucket_name, s3_key)

print(f"Uploaded Successfully to: s3://{bucket_name}/{s3_key}")