# LINE Audience Management Scripts

This repository contains scripts to manage audience groups for LINE using the Messaging API. The scripts allow you to create audience groups, upload user IDs to these groups, and update the `tabNames.csv` file with the generated audience group IDs.

## Prerequisites

- **Python**: Version 3.x
- **Python Libraries**: `requests` and `python-dotenv`
- **Configuration**: A `.env` file containing your LINE `CHANNEL_ACCESS_TOKEN`

## Setup

1. **Clone the Repository**:
```
git clone https://github.com/jerry914/LINE_audience.git
cd LINE_audience
```

2. **Install Required Libraries**:
```
pip install requests python-dotenv
```

3. **Configuration**:
Create a `.env` file in the root directory of the repository with the following content:
`CHANNEL_ACCESS_TOKEN=your_actual_channel_access_token`

Replace `your_actual_channel_access_token` with your actual LINE channel access token.

## Scripts

### 1. `upload_audience_group.py`

This script reads the `tagName` values from the `tabNames.csv` file and creates an audience group for each one using the LINE Messaging API. After creating an audience group, the script captures the `audienceGroupId` from the API response and updates the corresponding `tagID` in the `tabNames.csv` file.

**Usage**:
`python upload_audience_group.py`


### 2. `upload_user_ids.py`

This script reads user IDs from each file in the `TagAudience` directory and uploads them to the corresponding audience group using the LINE Messaging API.

**Usage**:
`python upload_user_ids.py`


## `tabNames.csv` Format

The `tabNames.csv` file should have the following format:
`tagID,tagName,keyword`

- `tagID`: The ID of the audience group (this will be updated by the `upload_audience_group.py` script).
- `tagName`: The name of the audience group.
- `keyword`: A keyword associated with the audience group (used in other functionalities).

## Notes

Ensure that the `tabNames.csv` file and the `TagAudience` directory are in the root directory of the repository before running the scripts.
