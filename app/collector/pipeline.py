import sqlite3
import yaml
from collector.sources.prometheus import PrometheusCollector


class MetricsPipeline:
    def __init__(self, config_path, db_path):
        self.config_path = config_path
        self.db_path = db_path
        self.config = self.load_config()
        self.collector = self.init_collector()

    def load_config(self):
        with open(self.config_path, "r") as file:
            return yaml.safe_load(file)

    def init_collector(self):
        collector_type = self.config["collector"]["type"]
        if collector_type == "prometheus":
            return PrometheusCollector(self.config["collector"])
        else:
            raise ValueError(f"Unsupported collector type: {collector_type}")

    def store_metrics(self, metrics):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        for metric in metrics:
            cursor.execute("""
                INSERT INTO api_metrics (service_name, api_name, metric_type, value, timestamp)
                VALUES (?, ?, ?, ?, ?)
            """, (metric["service_name"], metric["api_name"], metric["metric_type"], metric["value"], metric["timestamp"]))
        conn.commit()
        conn.close()

    def run(self):
        all_metrics = []
        for service in self.config["services"]:
            service_name = service["name"]
            for api in service["apis"]:
                api_name = api["name"]
                endpoint = api["endpoint"]
                metrics = self.collector.collect(service_name, api_name, endpoint)
                all_metrics.extend(metrics)
        self.store_metrics(all_metrics)
        print(f"Stored {len(all_metrics)} metrics.")