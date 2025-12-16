# Twitch IRC Bot

Template project for building Twitch chat bots in Python. Provides a basic command system and Twitch IRC connection.

## Project Structure

```
twitch-bot-template/
├── main.py              
├── requirements.txt       
├── .env.example           # Env variables example
├── commands/              
│   ├── __init__.py        # Command loader
│   ├── help.py            # Command example
├── twitch/                # Twitch IRC client
│   ├── __init__.py
│   ├── client.py          # Twitch IRC connection logic
│   ├── commands.py        # Command handler
├── README.md              
├── .gitignore             
```

## Creating Commands

Create a file in `commands/`:

```python
from twitch.commands import handler

@handler.command(name="ping", cooldown=5)
def ping(ctx):
    ctx.reply(f"Pong, {ctx.display_name}!")
```

### Options

| Option            | Type   | Description                          |
|-------------------|--------|--------------------------------------|
| `name`            | str    | Command name (default: function name) |
| `aliases`         | list   | Alternative names                    |
| `cooldown`        | int    | Seconds between uses per user        |
| `mod_only`        | bool   | Restrict to mods/broadcaster        |
| `broadcaster_only`| bool   | Restrict to broadcaster only         |

### Context Properties

| Property            | Type     | Description                                      |
|---------------------|----------|--------------------------------------------------|
| `ctx.username`      | str      | User's Twitch username                           |
| `ctx.display_name`  | str      | User's display name                              |
| `ctx.channel`       | str      | Channel where the command was used               |
| `ctx.args`          | list[str]| List of arguments after the command              |
| `ctx.is_mod`        | bool     | True if the user is a moderator                  |
| `ctx.is_sub`        | bool     | True if the user is a subscriber                 |
| `ctx.is_broadcaster`| bool     | True if the user is the channel owner            |
| `ctx.reply(text)`   | method   | Sends a message                                  |
