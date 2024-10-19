import os
import dotenv


dotenv.load_dotenv(dotenv.find_dotenv(usecwd=True))
BOT_TOKEN = os.getenv("BOT_TOKEN")