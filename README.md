# Cyber Scout

Telegram bot for basic domain analysis and web security checks.

This project collects basic information about a domain, including DNS data, HTTP response details, redirects, HTTPS status, security headers, and reputation results from external services.

## What it checks

- DNS and resolved IP address
- HTTP status code and server information
- Redirects
- HTTPS availability
- HSTS, CSP, and X-Frame-Options headers
- VirusTotal reputation
- Google Safe Browsing status

## Example

```text
/check google.com
```

Example response:

```text
Target: google.com

DNS
IP: 142.250.x.x

HTTP
Status: 200 OK
Server: gws
Redirect: 301 -> https://www.google.com/

Security
HTTPS: yes
HSTS: yes
CSP: no
X-Frame-Options: yes

VirusTotal: Clean
Detections: 0 / 91

Google Safe Browsing
Status: Clean
```

## Commands

| Command           | Description                        |
| ----------------- | ---------------------------------- |
| `/start`          | Show the welcome message           |
| `/help`           | Show available commands and checks |
| `/check <domain>` | Scan a domain                      |

## Stack

- Python 3
- [python-telegram-bot](https://python-telegram-bot.org/)
- [httpx](https://www.python-httpx.org/)
- [python-dotenv](https://github.com/theskumar/python-dotenv)
- VirusTotal API
- Google Safe Browsing API

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/scout0xaa/cyber-scout.git
cd cyber-scout
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows:

```powershell
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Create a `.env` file

```env
BOT_TOKEN=your_telegram_bot_token
VIRUSTOTAL_API_KEY=your_virustotal_api_key
GOOGLE_SAFE_BROWSING_KEY=your_google_safe_browsing_key
```

`BOT_TOKEN` is required. The external reputation checks require their corresponding API keys.

Do not commit `.env` or expose API keys publicly.

### 5. Run the bot

```bash
python bot.py
```

For development with automatic restarts:

```bash
pip install watchfiles
watchfiles --filter python "python bot.py"
```

## Project structure

```text
.
├── bot.py
├── config.py
├── requirements.txt
├── handlers/
│   ├── check.py
│   ├── help.py
│   └── start.py
└── services/
    ├── dns.py
    ├── google_safebrowsing.py
    ├── http.py
    ├── security.py
    └── virus_total_check.py
```

- `bot.py` creates the Telegram application and registers commands.
- `config.py` loads environment variables.
- `handlers/` contains Telegram command handlers.
- `services/` contains DNS, HTTP, security header, and reputation checks.
