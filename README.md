

# Twitch-bot-template

Template project for building Twitch chat bots in Python. Provides a simple command system and Twitch IRC connection.

## Project structure


```
twitch-bot-template/
├── main.py             
├── requirements.txt    
├── .env.example              # Example env file
├── commands/                 # Commands
│   ├── __init__.py
│   ├── help.py
│   ├── whois.py
├── twitch/                   # Twitch IRC
│   ├── __init__.py
│   ├── client.py             # Twitch IRC basic client
│   ├── message_handler.py    # Command registration and message parsing
├── README.md                
├── .gitignore                
```

## Command structure

```python
from twitch.message_handler import commands, PREFIX

@commands.add(name="ping", aliases=["p"], cooldown=5)
def ping(ctx):
    ctx.reply(f"Pong, {ctx.display_name}!")
```

## Context properties

| Property            | Type     | Description                                      |
|---------------------|----------|--------------------------------------------------|
| `ctx.username`      | str      | User's Twitch username                           |
| `ctx.display_name`  | str      | User's display name                              |
| `ctx.channel`       | str      | Channel where the command was used               |
| `ctx.args`          | list[str]| List of arguments after the command              |
| `ctx.is_mod`        | bool     | True if the user is a moderator                  |
| `ctx.is_sub`        | bool     | True if the user is a subscriber                 |
| `ctx.is_broadcaster`| bool     | True if the user is the channel owner            |
