# Clanguard

Clanguard is a Discord bot that manages and monitors your Clash Royale clan by fetching data from the Clash Royale API and posting updates on inactive members to a specified Discord channel.

## Features

- Fetches clan data from the Clash Royale API.
- Identifies inactive members based on specified thresholds.
- Posts a list of inactive members to a Discord channel weekly.

## Requirements

- Python 3.8+
- Discord account and a server to host the bot
- Clash Royale API token

## Setup

### 1. Clone the Repository

```sh
git clone https://github.com/yourusername/clanguard.git
cd clanguard
```

### 2. Create Virtual Environment

```sh
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Requirements
```sh
pip install -r requirements.txt
```

### 4. Setting Up Discord

1. Go to the Discord Developer Portal.

2. Click "New Application" and give it a name.

3. Navigate to the "Bot" tab and click "Add Bot".

4. Under "Token", click "Copy" to copy your bot token. You will need this token in the secrets.json file.

5. Navigate to the "OAuth2" tab, under "OAuth2 URL Generator", select bot under "scopes" and `Send Messages`, `Read Messages`,` Manage Messages` under "Bot Permissions".

5. Copy the generated URL, paste it into your browser, and invite the bot to your Discord server.

### 5. Setting Up Clash Royale API

1. Go to the Clash Royale API website.

2. Create an account and generate an API token.

### 6. Configuration Files

Create two JSON files in the root directory of the project: `secrets.json` and `config.json.`

Example of `secrets.json`
```json
{
    "discord_token": "YOUR_DISCORD_BOT_TOKEN",
    "channel_id": YOUR_DISCORD_CHANNEL_ID,
    "clash_royale_api_base": "https://api.clashroyale.com/v1",
    "clash_royale_token": "YOUR_CLASH_ROYALE_API_TOKEN"
}
```

Example of `config.json`
```json
{
    "clanID": "YOUR_CLAN_ID", # No Hashtag(#) needed
    "days_threshold": 7,
    "donation_threshold": 0,
    "clanChestPoints_threshold": 0
}
```
> Note: The comment # No Hashtag(#) needed is only for explanation and should not be included in your actual config.json file.

### 7. Running the Bot
```sh
python clanguard.py
```

## Project Structure
```arduino
clanguard/
│
├── models/
│   ├── config.py
│   ├── secret.py
│
├── venv/
│   ├── ...  # Virtual environment files
│
├── .gitignore
├── clanguard.py
├── config.json
├── fw.py
├── README.md
├── requirements.txt
├── secrets.json
```

## Models
`models/secret.py`
```python
from pydantic import BaseModel

class SecretModel(BaseModel):
    discord_token: str
    channel_id: int
    clash_royale_api_base: str
    clash_royale_token: str
```

`models/config.py`
```python
from pydantic import BaseModel

class ConfigModel(BaseModel):
    clanID: str
    days_threshold: int
    donation_threshold: int
    clanChestPoints_threshold: int
```

### License
This project is licensed under the MIT [License](https://opensource.org/license/MIT).
