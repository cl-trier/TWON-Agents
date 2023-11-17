from src import create_app
from src.config import Config

app = create_app(Config.load('./config.toml'))
