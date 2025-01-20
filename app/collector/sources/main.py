from abc import ABC, abstractmethod

class MetricsCollector(ABC):
    def __init__(self, config):
        self.config = config

    @abstractmethod
    def collect(self, service_name, api_name, endpoint):
        pass