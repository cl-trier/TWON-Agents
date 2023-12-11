from dotenv import load_dotenv

from src import create_app
from src.schemas import AppConfig

load_dotenv()

app = create_app(AppConfig.load('./config.toml'))
