from telegram import Update
from telegram.ext import CallbackContext
import time

class CommandHandler:
    def __init__(self, config_manager, firebase_manager):
        self.config_manager = config_manager
        self.firebase_manager = firebase_manager
        self.monitoring = False

    def start_command(self, update: Update, context: CallbackContext):
        active = self.config_manager.get_active_config()
        total = len(self.config_manager.list_configs())
        update.message.reply_text(
            f"🚀 Bot Active!\nFirebase Configs: {total}\nActive: {active['id'] if active else 'None'}"
        )

    def add_firebase(self, update: Update, context: CallbackContext):
        if not context.args:
            update.message.reply_text("⚠️ Usage: /addfirebase <url> [name]")
            return
        url = context.args[0].strip()
        name = " ".join(context.args[1:]) if len(context.args) > 1 else ""
        config_id = self.config_manager.add_config(url, name)
        update.message.reply_text(f"✅ Firebase {config_id} added!\nActive now.")

    def list_firebase(self, update: Update, context: CallbackContext):
        configs = self.config_manager.list_configs()
        active_id = self.config_manager.configs.get("active_id")
        if not configs:
            update.message.reply_text("📭 No Firebase configs.")
            return
        msg = "📋 Firebase Configs:\n\n"
        for cid, data in configs.items():
            status = "🟢" if cid == active_id else "🔴"
            msg += f"{status} ID: {cid} - {data.get('name', 'Unnamed')}\n"
        update.message.reply_text(msg)

    def use_firebase(self, update: Update, context: CallbackContext):
        if not context.args:
            update.message.reply_text("⚠️ Usage: /usefirebase <id>")
            return
        cid = context.args[0].strip()
        if self.config_manager.set_active_config(cid):
            update.message.reply_text(f"✅ Switched to Firebase {cid}")
        else:
            update.message.reply_text(f"❌ Firebase {cid} not found")

    def remove_firebase(self, update: Update, context: CallbackContext):
        if not context.args:
            update.message.reply_text("⚠️ Usage: /removefirebase <id>")
            return
        cid = context.args[0].strip()
        if self.config_manager.remove_config(cid):
            update.message.reply_text(f"✅ Firebase {cid} removed")
        else:
            update.message.reply_text(f"❌ Firebase {cid} not found")

    def start_monitor(self, update: Update, context: CallbackContext):
        self.monitoring = True
        update.message.reply_text("🟢 Monitoring started!")

    def stop_monitor(self, update: Update, context: CallbackContext):
        self.monitoring = False
        update.message.reply_text("🔴 Monitoring stopped!")

    def send_to_all(self, update: Update, context: CallbackContext):
        if not context.args:
            update.message.reply_text("⚠️ Usage: /sendall <message>")
            return
        message = " ".join(context.args)
        devices = self.firebase_manager.get_all_devices()
        if not devices:
            update.message.reply_text("❌ No devices found!")
            return
        success = 0
        for device_id in devices:
            if self.firebase_manager.send_command_to_device(device_id, message):
                success += 1
        update.message.reply_text(f"✅ Message sent to {success}/{len(devices)} devices")

    def status_command(self, update: Update, context: CallbackContext):
        active = self.config_manager.get_active_config()
        update.message.reply_text(
            f"📊 Status:\nActive: {active['id'] if active else 'None'}\nMonitoring: {self.monitoring}"
        )

    def help_command(self, update: Update, context: CallbackContext):
        help_text = """
📋 Commands:
/addfirebase <url> [name] - Add Firebase
/listfirebase - List all
/usefirebase <id> - Switch
/removefirebase <id> - Remove
/startmonitor - Start
/stopmonitor - Stop
/sendall <msg> - Send to all
/status - Status
/help - Help
"""
        update.message.reply_text(help_text)
