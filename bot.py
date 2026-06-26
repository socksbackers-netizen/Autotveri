import logging
from telegram.ext import Updater, CommandHandler
from config_manager import ConfigManager
from firebase_config import FirebaseManager
from commands import CommandHandler as BotCommands
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")

class Bot:
    def __init__(self):
        self.config_manager = ConfigManager()
        active = self.config_manager.get_active_config()
        if active:
            self.firebase_manager = FirebaseManager(active["url"])
        else:
            self.firebase_manager = None
        self.setup_handlers()

    def setup_handlers(self):
        self.updater = Updater(token=BOT_TOKEN, use_context=True)
        dp = self.updater.dispatcher
        cmd = BotCommands(self.config_manager, self.firebase_manager)
        handlers = [
            ("start", cmd.start_command),
            ("addfirebase", cmd.add_firebase),
            ("listfirebase", cmd.list_firebase),
            ("usefirebase", cmd.use_firebase),
            ("removefirebase", cmd.remove_firebase),
            ("startmonitor", cmd.start_monitor),
            ("stopmonitor", cmd.stop_monitor),
            ("sendall", cmd.send_to_all),
            ("status", cmd.status_command),
            ("help", cmd.help_command),
        ]
        for name, func in handlers:
            dp.add_handler(CommandHandler(name, func))

    def run(self):
        logger.info("Bot is running...")
        self.updater.start_polling()
        self.updater.idle()

if __name__ == "__main__":
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN not set! Please add it in Render environment variables.")
    else:
        Bot().run()
