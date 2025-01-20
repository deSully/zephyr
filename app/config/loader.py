import yaml

class ConfigLoader:
    def __init__(self, config_path):
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self):
        with open(self.config_path, 'r') as file:
            return yaml.safe_load(file)

    def get_collector_details(self):
        return self.config.get("collector", {})

    def get_services(self):
        return self.config.get("services", [])
