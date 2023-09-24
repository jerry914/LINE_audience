import csv
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BASE_URL = "https://api.line.me/v2/bot/audienceGroup/upload"
HEADERS = {
    "Authorization": f"Bearer {os.getenv('CHANNEL_ACCESS_TOKEN')}",
    "Content-Type": "application/json"
}
TAG_AUDIENCE_PATH = "TagAudience"

def read_user_ids_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        return [{"id": row[0]} for row in reader]

def upload_audience_from_file(filename):
    audience_name, audience_id = filename.replace('.csv', '').split('_')
    user_ids = read_user_ids_from_file(os.path.join(TAG_AUDIENCE_PATH, filename))
    
    payload = {
        "audienceGroupId": audience_id,
        "uploadDescription": audience_name,
        "audiences": user_ids
    }
    print(payload)

    response = requests.put(BASE_URL, headers=HEADERS, json=payload)
    
    if response.status_code == 202:
        print(f"Successfully uploaded user IDs for {audience_name}.")
    else:
        print(f"Error uploading user IDs for {audience_name}: {response.text}")

def main():
    for filename in os.listdir(TAG_AUDIENCE_PATH):
        if filename.endswith(".csv"):
            upload_audience_from_file(filename)

if __name__ == "__main__":
    main()
