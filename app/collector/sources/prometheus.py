import requests
from datetime import datetime
# Collecteur Prometheus
from collector.sources.main import MetricsCollector

class PrometheusCollector(MetricsCollector):
    def __init__(self, config):
        super().__init__(config)
        self.server_url = config.get("server_url")

    def collect(self, service_name, api_name, endpoint):
        queries = {
            "latency_95th": f'histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{{job="{service_name}"}}[5m]))',
            "success_rate": f'sum(rate(http_requests_total{{job="{service_name}", path="{endpoint}", status=~"2.."}}[5m])) / sum(rate(http_requests_total{{job="{service_name}", path="{endpoint}"}}[5m]))',
            "error_rate": f'sum(rate(http_requests_total{{job="{service_name}", path="{endpoint}", status=~"5.."}}[5m]))',
            "throughput": f'sum(rate(http_requests_total{{job="{service_name}", path="{endpoint}"}}[5m]))',
        }

        metrics = []
        for metric_name, query in queries.items():
            response = requests.get(f"{self.server_url}/api/v1/query", params={"query": query})
            response.raise_for_status()
            data = response.json().get("data", {}).get("result", [])
            for metric in data:
                metrics.append({
                    "service_name": service_name,
                    "api_name": api_name,
                    "metric_type": metric_name,
                    "value": float(metric["value"][1]),
                    "timestamp": datetime.fromtimestamp(float(metric["value"][0])),
                })
        return metrics
