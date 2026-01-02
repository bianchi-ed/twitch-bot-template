import os
import requests
from twitch.message_handler import commands
from datetime import datetime

PREFIX = os.getenv("COMMAND_PREFIX")

TWITCH_CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
TWITCH_USER_ACCESS_TOKEN = os.getenv("TWITCH_USER_ACCESS_TOKEN")

@commands.add(name="whois", cooldown=5)
def whois(ctx):
    if not ctx.args:
        ctx.reply(f"Usage: {PREFIX}whois <username>")
        return
    user = ctx.args[0]
    url = f"https://api.twitch.tv/helix/users?login={user}"
    headers = {
        "Client-ID": TWITCH_CLIENT_ID,
        "Authorization": f"Bearer {TWITCH_USER_ACCESS_TOKEN}"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        data = resp.json()
        if "data" in data and data["data"]:
            u = data["data"][0]
            created_at_us = u.get('created_at', '')
            if created_at_us:
                try:
                    dt = datetime.strptime(created_at_us, "%Y-%m-%dT%H:%M:%SZ")
                    created_at_us = dt.strftime("%m/%d/%Y")
                except Exception:
                    pass
            msg = (
                f"[ Username: {u['login']} ] "
                f"[ ID: {u['id']} ] "
                f"[ Broadcaster: {u.get('broadcaster_type', 'N/A')} ] "
                f"[ Created: {created_at_us} ] "
                f"[ Profile Pic: {u.get('profile_image_url', 'N/A')} ]"
            )
            ctx.reply(msg)
        else:
            ctx.reply(f"User '{user}' not found.")
    except Exception:
        ctx.reply("Error fetching user info.")
