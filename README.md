# discordBot

A single-guild Discord bot built with [discord.py](https://discordpy.readthedocs.io/).

## Features

- Slash commands: `/hello`, `/gang_sht`, `/test`, `/dm`
- Role assignment: `/assign1`, `/assign2`, `/remove1`, `/remove2`
- Reaction roles: `/reactionroles` (posts an embed with emoji reactions — role assignment on reaction is a work in progress)
- Legacy `!` prefix commands: `!reply`, `!poll`, `!secret1`, `!secret2`, `!secret3` (role-gated)
- Blacklisted-word filter that deletes offending messages
- Welcome DM on member join

## Setup

1. Create a virtual environment and install dependencies:
   ```
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Create a `.env` file in the project root:
   ```
   DISCORD_TOKEN=your_bot_token_here
   GUILD_ID=your_server_id_here
   ```

   - **DISCORD_TOKEN**: [Discord Developer Portal](https://discord.com/developers/applications) → your application → **Bot** tab → Reset/Copy Token
   - **GUILD_ID**: enable Developer Mode in Discord (Settings → Advanced), then right-click your server icon → Copy Server ID

3. Invite the bot to your server via **OAuth2 → URL Generator** in the Developer Portal, with the `bot` and `applications.commands` scopes and the permissions your commands need (e.g. Manage Roles, Send Messages).

4. Create a `bad_words.py` file in the project root defining the word filter list:
   ```python
   blacklisted_words = []
   ```

## Running

```
source venv/bin/activate
python3 main.py
```

Logs are written to `discord.log`.

## Tests

```
python3 -m pytest tests/
```
