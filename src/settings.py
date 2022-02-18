import os
from pprint import pprint
import sys

STAGE = os.getenv("STAGE") or (sys.argv[1] if (len(sys.argv) == 2) else "") or "dev"
print(f"STAGE: {STAGE}")

config = {}

config["KEY"] = os.getenv("VALUE")
config["KEY"] = os.getenv("VALUE")

if STAGE == "prod":
    config["KEY"] = "VALUE"

elif STAGE == "dev":
    config["KEY"] = "VALUE"


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

    def add(self, k: dict):
        self.__dict__.update(k)


env = Struct(**config)
# print(dir(env), '\n', env.REDSHIFT_HOST)
