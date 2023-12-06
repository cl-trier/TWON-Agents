from dotenv import load_dotenv

from src import create_app
from src.config import Config

load_dotenv()

app = create_app(Config.load('./config.toml'))
