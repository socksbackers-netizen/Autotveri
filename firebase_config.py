import requests
import time

class FirebaseManager:
    def __init__(self, database_url):
        self.database_url = database_url

    def get_all_devices(self):
        try:
            url = f"{self.database_url}/devices.json"
            response = requests.get(url)
            if response.status_code == 200:
                return response.json() if response.json() else {}
            return {}
        except Exception as e:
            print(f"Error fetching devices: {e}")
            return {}

    def send_command_to_device(self, device_id, command):
        try:
            url = f"{self.database_url}/devices/{device_id}/command.json"
            data = {
                "command": command,
                "timestamp": int(time.time()),
                "status": "pending"
            }
            response = requests.put(url, json=data)
            return response.status_code == 200
        except Exception as e:
            print(f"Error sending command: {e}")
            return False

    def update_log(self, log_data):
        try:
            url = f"{self.database_url}/logs.json"
            response = requests.post(url, json=log_data)
            return response.status_code == 200
        except Exception as e:
            print(f"Error updating log: {e}")
            return False
