import csv
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

BASE_URL = "https://api.line.me/v2/bot/audienceGroup/upload"
HEADERS = {
    "Authorization": f"Bearer {os.getenv('CHANNEL_ACCESS_TOKEN')}",
    "Content-Type": "application/json"
}
TAB_NAMES_FILE = "tabNames.csv"

def read_tab_names():
    with open(TAB_NAMES_FILE, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        return list(reader)

def create_audience_group(audience_group_name):
    payload = {
        "description": audience_group_name
    }

    response = requests.post(BASE_URL, headers=HEADERS, json=payload)
    
    if response.status_code == 202:
        print(f"Successfully created audience group: {audience_group_name}.")
        return response.json()["audienceGroupId"]
    else:
        print(f"Error creating audience group {audience_group_name}: {response.text}")
        return None

def update_tab_names_with_audience_group_id(data):
    with open(TAB_NAMES_FILE, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["tagID", "tagName", "keyword"])  # Write header
        writer.writerows(data)

def main():
    tab_names_data = read_tab_names()
    for row in tab_names_data:
        tagID, tagName, _ = row
        audience_group_id = create_audience_group(tagName)
        if audience_group_id:
            row[0] = audience_group_id  # Update tagID with audienceGroupId
    update_tab_names_with_audience_group_id(tab_names_data)

if __name__ == "__main__":
    main()
