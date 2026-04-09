# Telegram Referral Bot

> Automate referral invitations on Telegram by emulating the `/start` command with your referral code across multiple accounts.

![Screenshot](https://github.com/svtcore/telegram-referral-bot/blob/main/screenshot.PNG)
---

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Preparing Accounts](#preparing-accounts)
- [Proxy Support](#proxy-support)
- [Usage](#usage)
- [CLI Reference](#cli-reference)
- [Project Structure](#project-structure)
- [Contributing](#contributing)

---

## Features

- Sends `/start <referral_code>` to any Telegram bot on behalf of multiple accounts
- Supports both **session files** and **Pyrogram string sessions**
- Optional **channel auto-join** before sending the referral command
- **Proxy support** (anonymous and authenticated)
- Configurable **random delay** between accounts to avoid rate limits
- **Interactive mode** – no flags needed, the script prompts for everything

---

## Requirements

- Python 3.10+
- Telegram API credentials (`api_id` and `api_hash`) for each account, obtained from [my.telegram.org](https://my.telegram.org)

---

## Installation

```bash
git clone https://github.com/svtcore/telegram-referral-bot.git
cd telegram-referral-bot
pip install -r requirements.txt
```

---

## Configuration

Copy the example env file and fill in your values:

```bash
cp .env.example .env
```

| Variable | Required | Description |
|---|---|---|
| `BOT_NAME` | Yes | Bot username **without** `@` (e.g. `my_bot`) |
| `COUNT` | Yes | Number of accounts to use |
| `REFER_ID` | Yes | Your referral code – from `t.me/my_bot?start=`**`12345`**, enter only `12345` |
| `DELAY_MIN` | No | Minimum delay in seconds between accounts (default: `10`) |
| `DELAY_MAX` | No | Maximum delay in seconds between accounts (default: `15`) |
| `CHANNEL_NAME` | No | Channel username to join before sending `/start` (without `@`) |

**Example `.env`:**

```env
BOT_NAME=my_new_coin_bot
COUNT=5
REFER_ID=111222333
CHANNEL_NAME=my_new_coin_channel
DELAY_MIN=10
DELAY_MAX=15
```

---

## Preparing Accounts

Create a plain-text file (e.g. `accounts.txt`) – one account per line.

### Option A – Session files (requires authorization step)

Format: `SESSION_NAME:API_ID:API_HASH`

```
MY_ACCOUNT_1:11223344:d54d1702ad0f8326224b817c796763c9
MY_ACCOUNT_2:55667788:a91c3401be1f9437335c928de905874f
```

After filling in `accounts.txt`, run the authorization step once to generate session files in the `sessions/` folder:

```bash
python bot.py --auth -t accounts.txt
```

### Option B – Pyrogram string sessions (no authorization step needed)

Paste each string session on its own line, no extra formatting required:

```
AQEAbCdEfG...
AQEAxYzWvU...
```

> All account/proxy files must be placed in the **root of the project folder**.

---

## Proxy Support

Create a plain-text file (e.g. `proxies.txt`) – one proxy per line.

```
# No proxy – leave the file empty, or omit --proxies flag

# Anonymous proxy
192.168.1.1:8080

# Authenticated proxy
192.168.1.1:8080:login:password
```

---

## Usage

### 1. Authenticate accounts (session files only)

```bash
python bot.py --auth -t accounts.txt
```

### 2. Run the referral bot

```bash
# Standard run
python bot.py --run -t accounts.txt

# With string sessions
python bot.py --run -t accounts.txt --strings

# With proxies
python bot.py --run -t accounts.txt -p proxies.txt

# With channel join (requires CHANNEL_NAME set in .env)
python bot.py --run -t accounts.txt --channel

# All options combined
python bot.py --run -t accounts.txt -p proxies.txt --channel
```

### 3. Interactive mode

Prompts for all settings step by step – no flags needed:

```bash
python bot.py --interactive
```

---

## CLI Reference

| Flag | Short | Description |
|---|---|---|
| `--auth` | `-a` | Authenticate accounts and create session files |
| `--run` | `-r` | Run the referral bot |
| `--interactive` | `-i` | Start in interactive mode |
| `--tokens FILE` | `-t` | Path to the accounts file |
| `--proxies FILE` | `-p` | Path to the proxies file |
| `--strings` | `-s` | Use Pyrogram string sessions instead of session files |
| `--channel` | `-ch` | Join the channel configured in `.env` before sending `/start` |

---

## Contributing

Pull requests are welcome. For significant changes, please open an issue first to discuss what you would like to change.
If the script returns an error, open an issue with the provided error message 

## License
[MIT](https://github.com/svtcore/telegram-referral-bot/blob/main/LICENSE)

## Involved libraries
* [Pyrogram](https://github.com/pyrogram/pyrogram)
* [python-dotenv](https://github.com/theskumar/python-dotenv)

## Responsibility
All materials are provided for educational purposes only. The author does not bear the responsibility of the consequences of use by other users
