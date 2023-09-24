import requests
import time
import os
from dotenv import load_dotenv
import csv

# Load environment variables from .env file
load_dotenv()

BASE_URL = "https://api.line.me/v2/bot"
HEADERS = {
    "Authorization": f"Bearer {os.getenv('CHANNEL_ACCESS_TOKEN')}"  # Read from .env file
}
RATE_LIMIT = 1000  # requests per second
SLEEP_TIME = 1 / RATE_LIMIT  # time to sleep between requests to avoid rate limit

def get_followers_ids(start=None):
    params = {"limit": 1000}
    if start:
        params["start"] = start

    response = requests.get(f"{BASE_URL}/followers/ids", headers=HEADERS, params=params)
    response_data = response.json()

    return response_data.get("userIds", []), response_data.get("next", None)

def get_user_profile(user_id):
    response = requests.get(f"{BASE_URL}/profile/{user_id}", headers=HEADERS)
    return response.json()

def main():
    all_user_ids = []
    next_start = None

    while True:
        user_ids, next_start = get_followers_ids(next_start)
        all_user_ids.extend(user_ids)

        if not next_start:
            break

        time.sleep(SLEEP_TIME)  # To ensure we don't hit the rate limit

    all_users_profiles = []

    for user_id in all_user_ids:
        profile = get_user_profile(user_id)
        all_users_profiles.append(profile)
        print(profile)
        time.sleep(SLEEP_TIME)  # To ensure we don't hit the rate limit

    # Write userID and username to a CSV file
    with open('users.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["userID", "username"])  # Write header

        for profile in all_users_profiles:
            writer.writerow([profile["userId"], profile["displayName"]])


if __name__ == "__main__":
    main()
