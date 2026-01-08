![Version](https://img.shields.io/badge/version-v1.01--alpha-blue?style=for-the-badge)
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
```


4. **Run the Bot**
```bash
python main.py
```
---

## 📝 Update Log

### [v1.01-alpha] - 2026-01-07
- **Feature**: Real-time Devpost API integration (1-hour interval).
- **Feature**: Automated duplicate alert prevention using JSON database.
- **Bot**: Added `!ping` command to check bot health status.
- **Safety**: Implemented emergency self-shutdown & auto-restart logic on Railway.
- **System**: Optimized directory structure and environment variable management.