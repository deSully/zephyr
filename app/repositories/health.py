import sqlite3

class HealthRepository:
    def __init__(self):
        self.db_path = "app/data/metrics.db"  # Assurez-vous que le chemin est correct.

    def get_health_status(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Vérifie si les tables existent
            cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table';")
            tables_exist = cursor.fetchone()[0] > 0

            if not tables_exist:
                return False, {}

            # Compte les enregistrements dans les tables principales
            stats = {}
            for table in ["services", "operations", "metrics"]:
                cursor.execute(f"SELECT COUNT(*) FROM {table};")
                stats[table] = cursor.fetchone()[0]

            conn.close()
            return True, stats
        except sqlite3.Error:
            return False, {}
