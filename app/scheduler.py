from apscheduler.schedulers.background import BackgroundScheduler
from app.config.loader import ConfigLoader
from collector.pipeline import MetricsPipeline
from ml.train import ModelTrainer


class JobManager:
    def __init__(self, config_path, db_path, results_path):
        self.config = ConfigLoader(config_path)
        self.db_path = db_path
        self.results_path = results_path
        self.scheduler = BackgroundScheduler()

    def start_jobs(self):
        # Initialisation de la pipeline
        pipeline = MetricsPipeline(self.config.config_path, self.db_path)

        # Ajouter des jobs pour chaque API avec son cron
        for service in self.config.get_services():
            for api in service["apis"]:
                cron = api.get("cron")
                if cron:
                    self.scheduler.add_job(
                        pipeline.run,  # Lancer la collecte et le stockage des métriques
                        "cron",
                        **self._parse_cron(cron),
                        args=[],
                        id=f'{service["name"]}-{api["name"]}'
                    )

        # Ajouter un job pour l'entraînement
        train_cron = self.config.config["train"]["cron"]
        self.scheduler.add_job(
            self.train_model,  # Appeler la fonction dédiée à l'entraînement
            "cron",
            **self._parse_cron(train_cron),
            id="train-job"
        )

        # Démarrer le planificateur
        self.scheduler.start()

    def train_model(self):
        # Appeler la logique d'entraînement
        trainer = ModelTrainer(self.db_path, self.results_path)
        trainer.train_and_save_model()
        print("Training completed and model saved.")

    def _parse_cron(self, cron_expression):
        """Convertit l'expression cron en arguments pour APScheduler."""
        minute, hour, day, month, day_of_week = cron_expression.split()
        return {
            "minute": minute,
            "hour": hour,
            "day": day,
            "month": month,
            "day_of_week": day_of_week,
        }
