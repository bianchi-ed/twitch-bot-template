import os
import re
from collections import defaultdict

PREFIX = os.getenv("COMMAND_PREFIX", "!")


class MessageHandler:
    def __init__(self):
        self._commands = {}
        self._cooldowns = defaultdict(dict)

    def command(self, name=None, aliases=None, cooldown=0, mod_only=False, broadcaster_only=False):
        def decorator(func):
            cmd_name = name or func.__name__
            options = {
                "aliases": aliases or [],
                "cooldown": cooldown,
                "mod_only": mod_only,
                "broadcaster_only": broadcaster_only
            }
            self.register_command(cmd_name, func, **options)
            return func
        return decorator

    def register_command(self, name, func, **options):
        self._commands[name] = {"func": func, "options": options}
        for alias in options.get("aliases", []):
            self._commands[alias] = self._commands[name]

    def on_message(self, message, client):
        text = message.get("text", "")
        if text.startswith(PREFIX):
            print(f"[{PREFIX}] <{message['display_name']}> {message['text']}")
            self.handle_command(message, client)
        else:
            self.handle_general_message(message, client)

    def handle_command(self, message, client):
        text = message["text"][len(PREFIX):]
        if not text:
            return
        parts = text.split()
        cmd = parts[0].lower()
        args = parts[1:]
        if cmd in self._commands:
            ctx = self._build_context(message, client, args)
            self._commands[cmd]["func"](ctx)

    def get_all(self):
        # Return only unique command names (not aliases)
        return [name for name, v in self._commands.items() if v["func"].__name__ == name]

    def handle_general_message(self, message, client):
        # Print non-command messages to the console
        print(f"<{message['display_name']}> {message['text']}")

    def _build_context(self, message, client, args):
        class Ctx:
            def __init__(self):
                self.username = message["username"]
                self.display_name = message["display_name"]
                self.channel = message["channel"]
                self.args = args
                self.is_mod = message.get("is_mod", False)
                self.is_sub = message.get("is_sub", False)
                self.is_broadcaster = message["username"].lower() == message["channel"].lower()
                self.bot_username = getattr(client, "bot_username", os.getenv("TWITCH_BOT_USERNAME", "bot"))

            def reply(self, text):
                client.send_message(self.channel, text)
                print(f"[{PREFIX}] <{self.bot_username}> {text}")
        return Ctx()

handler = MessageHandler()