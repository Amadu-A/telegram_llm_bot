from environs import Env


env = Env()
env.read_env()

TELEGRAM_BOT_TOKEN = env.str("BOT_TOKEN")
DATABASE_URL = "sqlite:///./bot_data.db"
YANDEX_API_KEY = env.str("YANDEX_API_KEY")
FOLDER_ID = env.str("FOLDER_ID")
