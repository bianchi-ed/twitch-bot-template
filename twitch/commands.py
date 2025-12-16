# Command handler

import os
import time

PREFIX = os.getenv("COMMAND_PREFIX", "!")


class CommandContext:
    def __init__(self, message, client, args):
        self.username = message["username"]
        self.display_name = message["display_name"]
        self.channel = message["channel"]
        self.user_id = message["user_id"]
        self.is_mod = message["is_mod"]
        self.is_sub = message["is_sub"]
        self.is_broadcaster = message["username"].lower() == message["channel"].lower()
        self.args = args
        self._client = client
    
    def reply(self, text):
        self._client.send_message(self.channel, text)
        print(f"[>] {text}")


class CommandHandler:
    def __init__(self):
        self._commands = {}
        self._cooldowns = {}
    
    def command(self, name=None, aliases=None, cooldown=0, mod_only=False, broadcaster_only=False):
        def decorator(func):
            command_name = name or func.__name__
            self._commands[command_name] = {
                "func": func,
                "cooldown": cooldown,
                "mod_only": mod_only,
                "broadcaster_only": broadcaster_only
            }
            for alias in (aliases or []):
                self._commands[alias] = self._commands[command_name]
            print(f"[+] !{command_name}")
            return func
        return decorator
    
    def on_message(self, message, client):
        text = message["text"]
        print(f"<{message['display_name']}> {text}")
        
        if not text.startswith(PREFIX):
            return
        
        parts = text[len(PREFIX):].split()
        if not parts:
            return
        
        command = self._commands.get(parts[0].lower())
        if not command:
            return
        
        ctx = CommandContext(message, client, parts[1:])
        
        if command["broadcaster_only"] and not ctx.is_broadcaster:
            return
        if command["mod_only"] and not (ctx.is_mod or ctx.is_broadcaster):
            return
        
        cooldown_key = f"{message['user_id']}:{parts[0]}"
        if command["cooldown"] > 0:
            if time.time() - self._cooldowns.get(cooldown_key, 0) < command["cooldown"]:
                return
            self._cooldowns[cooldown_key] = time.time()
        
        try:
            command["func"](ctx)
        except Exception as error:
            print(f"[!] {error}")
    
    def get_all(self):
        seen = set()
        for name, command in self._commands.items():
            if id(command) not in seen:
                seen.add(id(command))
                yield name


handler = CommandHandler()
