import tomllib

from src import create_app

app = create_app(tomllib.load(open("config.toml", "rb")))
