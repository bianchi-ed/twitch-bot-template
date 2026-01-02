import os
import re
from collections import defaultdict

PREFIX = os.getenv("COMMAND_PREFIX")

class ChatCommands:
    def __init__(self):
        self.command_map = {}
        self.user_cooldowns = defaultdict(dict)

    def add(self, name=None, aliases=None, cooldown=0, mod_only=False, broadcaster_only=False):
        def decorator(func):
            cmd_name = name or func.__name__
            options = {
                "aliases": aliases or [],
                "cooldown": cooldown,
                "mod_only": mod_only,
                "broadcaster_only": broadcaster_only
            }
            self.add_command(cmd_name, func, **options)
            return func
        return decorator

    def add_command(self, name, func, **options):
        self.command_map[name] = {"func": func, "options": options}
        for alias in options.get("aliases", []):
            self.command_map[alias] = self.command_map[name]

    def handle(self, message, client):
        text = message.get("text", "")
        if text.startswith(PREFIX):
            print(f"[{PREFIX}] <{message['display_name']}> {message['text']}")
            self.run(message, client)
        else:
            self.show(message, client)

    def run(self, message, client):
        text = message["text"][len(PREFIX):]
        if not text:
            return
        parts = text.split()
        cmd = parts[0].lower()
        args = parts[1:]
        if cmd in self.command_map:
            ctx = self.make_context(message, client, args)
            self.command_map[cmd]["func"](ctx)

    def list(self):
        return [name for name, v in self.command_map.items() if v["func"].__name__ == name]

    def show(self, message, client):
        print(f"<{message['display_name']}> {message['text']}")

    def make_context(self, message, client, args):
        class Ctx:
            def __init__(self):
                self.username = message["username"]
                self.display_name = message["display_name"]
                self.channel = message["channel"]
                self.args = args
                self.is_mod = message.get("is_mod", False)
                self.is_sub = message.get("is_sub", False)
                self.is_broadcaster = message["username"].lower() == message["channel"].lower()

            def reply(self, text):
                client.send_message(self.channel, text)
                print(f"[{PREFIX}] <{self.bot_username}> {text}")
        return Ctx()

commands = ChatCommands()