from types import SimpleNamespace
import json

with open("config.json", "r") as _:
    CONFIG = json.load(_, object_hook=lambda item: SimpleNamespace(**item))

# Files
TEMPLATES = CONFIG.templates.folder

print(TEMPLATES)
