import csv
import os

# Paths
CHAT_HISTORY_PATH = "ChatHistory"
TAG_AUDIENCE_PATH = "TagAudience"
KEYWORDS_FILE = "tabNames.csv"
USERS_FILE = "users.csv"

def read_keywords():
    keywords_map = {}
    with open(KEYWORDS_FILE, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        for row in reader:
            tagID, tagName, keyword = row
            keywords_map[keyword] = (tagID, tagName)
    return keywords_map

def get_existing_user_ids(tagName, tagID):
    tag_file = os.path.join(TAG_AUDIENCE_PATH, f"{tagName}_{tagID}.csv")
    if os.path.exists(tag_file):
        with open(tag_file, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            return set(row[0] for row in reader)
    return set()

def map_username_to_userid():
    user_map = {}
    with open(USERS_FILE, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        for row in reader:
            userID, username = row
            user_map[username] = userID
    return user_map

def process_chat_files(keywords_map, user_map):
    for filename in os.listdir(CHAT_HISTORY_PATH):
        if filename.endswith(".csv"):
            filepath = os.path.join(CHAT_HISTORY_PATH, filename)
            with open(filepath, 'r', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    # Check if row[4] exists
                    if len(row) > 4:
                        for keyword, (tagID, tagName) in keywords_map.items():
                            if keyword in row[4]:  # Check if keyword is contained in the column
                                existing_user_ids = get_existing_user_ids(tagName, tagID)
                                username = filename.split('_')[2].replace('.csv', '')
                                user_id = user_map.get(username)
                                if user_id and user_id not in existing_user_ids:
                                    tag_file = os.path.join(TAG_AUDIENCE_PATH, f"{tagName}_{tagID}.csv")
                                    with open(tag_file, 'a', newline='', encoding='utf-8') as tagfile:
                                        writer = csv.writer(tagfile)
                                        writer.writerow([user_id])

if __name__ == "__main__":
    keywords_map = read_keywords()
    user_map = map_username_to_userid()
    process_chat_files(keywords_map, user_map)
