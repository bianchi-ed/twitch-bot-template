import os
import glob
import importlib


def load_commands():
    d = os.path.dirname(__file__)
    for f in glob.glob(os.path.join(d, "*.py")):
        n = os.path.basename(f)[:-3]
        if not n.startswith("_"):
            try:
                importlib.import_module(f"commands.{n}")
            except Exception as e:
                print(f"[!] {n}: {e}")
