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
TO-DO

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


3. **Configure Environment Variables**
Create a `.env` file in the root directory and enter your bot token.
```env
DISCORD_TOKEN=your_bot_token_here

```


4. **Run the Bot**
```bash
python main.py

```



## ⌨️ Usage
* TBD
