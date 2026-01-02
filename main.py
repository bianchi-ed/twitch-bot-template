import signal
import sys
from dotenv import load_dotenv

load_dotenv()

from twitch.client import TwitchClient
from twitch.message_handler import commands
from commands import load_commands

_client = None


def shutdown(sig=None, frame=None):
    if _client:
        _client.stop()
    sys.exit(0)


def main():
    global _client
    signal.signal(signal.SIGINT, shutdown)
    
    load_commands()
    _client = TwitchClient(commands.handle)
    
    try:
        _client.run()
    except KeyboardInterrupt:
        shutdown()
    except Exception as e:
        print(f"[!] Error: {e}")
        shutdown()


if __name__ == "__main__":
    main()
