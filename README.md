![Version](https://img.shields.io/badge/version-v1.02--alpha-blue?style=for-the-badge)
![Status](https://img.shields.io/badge/status-active-success?style=for-the-badge)
---

# 🤖 Devpost Hackathon Discord Bot

This project is a Python-based Discord bot that utilizes the **Devpost API** to collect the latest hackathon information and announce it in a clean "Card" (Embed) format to a Discord server.

## 📌 Key Features

* **Data Collection**: Fetches real-time hackathon data via the official Devpost API.
* **Detailed Parsing**: Extracts Title, Link, Thumbnail, Status, Location, Prize (Cash/Other breakdown), Host, Period, and Themes.
* **Discord Embeds**: Uses Discord's Embed design to send collected information with high readability.

## 🛠 Tech Stack

* **Language**: Python 3.9+
* **Libraries**: `discord.py`, `requests`, `python-dotenv`
* **Data Format**: JSON (Devpost API)

## 📂 Project Structure

```text
├── cogs/                # Bot extensions (cogs)
│   └── hackathon.py     # Main hackathon alert logic
├── main.py              # Entry point of the bot
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

## 🚀 Getting Started

### 1. Prerequisites

* Python must be installed on your system.
* You need to create a bot account and obtain the token.

### 2. Installation & Execution

1. **Create and Activate a Virtual Environment**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```


2. **Install Required Libraries**
```bash
pip install discord.py requests python-dotenv
```

or 
```bash
pip install -r requirements.txt
```


3. **Configure Environment Variables**
Create a `.env` file in the root directory and enter your bot token.
```env
DISCORD_TOKEN=your_bot_token_here
CHANNEL_ID=the_channel_ID_run_the_bot
ENABLED_COGS=the_features_you_test
```


4. **Run the Bot**
```bash
python main.py
```
---

## 📝 Update Log

### [v1.02-alpha] - 2026-01-08
**Major Feature Update & UI Overhaul**

- **✨ New Command: `!hack`**
  - Manually triggers a fetch for the **top 3 trending hackathons** from Devpost.
  - Displays them immediately and adds unique items to the database (prevents duplicates).
  - Does not interfere with the automatic 1-hour timer loop.

- **📊 Enhanced Command: `!db`**
  - **Full List Display**: No longer hides data. Displays **all** stored hackathon URLs.
  - **Pagination**: Automatically splits the list into chunks (10 items per message) to bypass Discord's character limits.

- **🎨 UI/UX Improvements**
  - **Advanced Embed Design**: Fully redesigned notification cards to match real Devpost API data.
    - Added fields: `📍 Location`, `🏢 Host`, `📅 Period`, `💰 Prize (Cash/Other)`, `🏷️ Themes`.
  - **Alert Visibility**: Added a plain text **"New Hackathon Alert!"** message before the embed to ensure users get notified via push notifications.
  - **Startup Notification**: The bot now sends a *"🚀 System Online"* message to the designated channel upon a successful reboot or deployment.

- **⚙️ Internal Logic**
  - Refined JSON parsing logic to handle complex Devpost API structures (nested locations, prize counts, themes).
  - Optimized error handling for manual commands.

### [v1.01-alpha] - 2026-01-07
- **Feature**: Real-time Devpost API integration (1-hour interval).
- **Feature**: Automated duplicate alert prevention using JSON database.
- **Bot**: Added `!ping` command to check bot health status.
- **Safety**: Implemented emergency self-shutdown & auto-restart logic on Railway.
- **System**: Optimized directory structure and environment variable management.
