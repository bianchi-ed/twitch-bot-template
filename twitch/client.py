# Twitch IRC client

import os
import re
import socket


class TwitchClient:
    
    def __init__(self, on_message_callback):
        self._socket = None
        self._on_message_callback = on_message_callback
        self._channels = []
        self._is_running = False
        self.bot_username = None
    
    def _get_required_env(self, name):
        value = os.getenv(name)
        if not value:
            raise ValueError(f"Missing required environment variable: {name}")
        return value
    
    def run(self):
        server = self._get_required_env("TWITCH_SERVER")
        try:
            port = int(self._get_required_env("TWITCH_PORT"))
        except ValueError:
            raise ValueError("TWITCH_PORT must be a valid integer")
        oauth_token = self._get_required_env("TWITCH_OAUTH_TOKEN")
        bot_username = self._get_required_env("TWITCH_BOT_USERNAME")
        self.bot_username = bot_username
        self._channels = [channel.strip() for channel in os.getenv("TWITCH_CHANNELS", "").split(",") if channel.strip()]
        
        if not self._channels:
            raise ValueError("TWITCH_CHANNELS must contain at least one channel")
        
        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.connect((server, port))
            self._socket.settimeout(1.0)
        except socket.error as e:
            if self._socket:
                self._socket.close()
                self._socket = None
            raise ConnectionError(f"Failed to connect to Twitch IRC: {e}")
        
        self._send(f"PASS {oauth_token}")
        self._send(f"NICK {bot_username}")
        self._send("CAP REQ :twitch.tv/tags twitch.tv/commands")
        
        for channel in self._channels:
            self._send(f"JOIN #{channel}")
            print(f"[+] #{channel}")
        
        self._is_running = True
        self._listen()
    
    def _send(self, raw_message):
        self._socket.send(f"{raw_message}\r\n".encode())
    
    def _listen(self):
        buffer = ""
        while self._is_running:
            try:
                buffer += self._socket.recv(4096).decode()
            except socket.timeout:
                continue
            except Exception as e:
                print(f"[!] Connection error: {e}")
                self._is_running = False
                break
            
            lines = buffer.split("\r\n")
            buffer = lines.pop()
            
            for line in lines:
                if not line:
                    continue
                if line.startswith("PING"):
                    self._send(f"PONG{line[4:]}")
                elif "PRIVMSG" in line:
                    message = self._parse_message(line)
                    if message:
                        self._on_message_callback(message, self)
    
    def _parse_message(self, raw_line):
        tags = {}
        if raw_line.startswith("@"):
            separator_index = raw_line.index(" ")
            for tag in raw_line[1:separator_index].split(";"):
                if "=" in tag:
                    key, value = tag.split("=", 1)
                    tags[key] = value
            raw_line = raw_line[separator_index + 1:]
        
        match = re.match(r":(\w+)!\S+ PRIVMSG #(\w+) :(.*)", raw_line)
        if not match:
            return None
        
        username = match.group(1)
        return {
            "username": username,
            "display_name": tags.get("display-name", username),
            "channel": match.group(2),
            "text": match.group(3),
            "user_id": tags.get("user-id", ""),
            "is_mod": tags.get("mod") == "1",
            "is_sub": tags.get("subscriber") == "1"
        }
    
    def send_message(self, channel, text):
        self._send(f"PRIVMSG #{channel} :{text}")
    
    def stop(self):
        self._is_running = False
        for channel in self._channels:
            self._send(f"PART #{channel}")
        if self._socket:
            self._socket.close()
        print("[-] Disconnected")
