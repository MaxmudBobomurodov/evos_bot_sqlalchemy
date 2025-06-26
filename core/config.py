import os

from dotenv import load_dotenv

load_dotenv(
    dotenv_path=".env"
)

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

TOKEN = os.getenv("TOKEN")
DEVELOPER = 5894214924
ADMINS = [5894214924]


CHANNELS = [
    {
        "name" : "Channel 1",
        "link" : "https://t.me/+AyDEusSfUrA5ZjMy",
        "chat_id": -1002356666639
    }
]


I18N_DOMAIN = 'lang'
LOCALES_DIR = 'locale'

DB_CONFIG = {
    "database": DB_NAME,
    "user": DB_USER,
    "port": DB_PORT,
    "host": DB_HOST,
    "password": DB_PASS
}
