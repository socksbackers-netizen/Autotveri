import json
import os
from datetime import datetime

class ConfigManager:
    def __init__(self):
        self.config_file = "firebase_configs.json"
        self.load_configs()

    def load_configs(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                self.configs = json.load(f)
        else:
            self.configs = {
                "active_id": None,
                "configs": {}
            }
        self.save_configs()

    def save_configs(self):
        with open(self.config_file, "w") as f:
            json.dump(self.configs, f, indent=2)

    def add_config(self, url, name=""):
        config_id = len(self.configs["configs"]) + 1
        self.configs["configs"][str(config_id)] = {
            "id": config_id,
            "url": url,
            "name": name or f"Firebase {config_id}",
            "added": datetime.now().isoformat()
        }
        self.configs["active_id"] = str(config_id)
        self.save_configs()
        return config_id

    def get_active_config(self):
        active_id = self.configs.get("active_id")
        if active_id and active_id in self.configs["configs"]:
            return self.configs["configs"][active_id]
        return None

    def set_active_config(self, config_id):
        if str(config_id) in self.configs["configs"]:
            self.configs["active_id"] = str(config_id)
            self.save_configs()
            return True
        return False

    def list_configs(self):
        return self.configs["configs"]

    def remove_config(self, config_id):
        if str(config_id) in self.configs["configs"]:
            del self.configs["configs"][str(config_id)]
            if self.configs["active_id"] == str(config_id):
                self.configs["active_id"] = None
            self.save_configs()
            return True
        return False
