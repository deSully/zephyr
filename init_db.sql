-- Création de la table des services
CREATE TABLE IF NOT EXISTS services (
                                        id INTEGER PRIMARY KEY,
                                        name TEXT NOT NULL,
                                        description TEXT,
                                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Création de la table des opérations (ou appels API)
CREATE TABLE IF NOT EXISTS operations (
                                          id INTEGER PRIMARY KEY,
                                          service_id INTEGER,
                                          name TEXT NOT NULL,
                                          description TEXT,
                                          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                          FOREIGN KEY (service_id) REFERENCES services(id)
    );

-- Création de la table des métriques de performance (latence, erreurs, etc.)
CREATE TABLE IF NOT EXISTS api_metrics (
                                           id INTEGER PRIMARY KEY,
                                           operation_id INTEGER,
                                           metric_type TEXT NOT NULL,  -- Ajout de la colonne metric_type
                                           value REAL NOT NULL,        -- Ajout de la colonne value
                                           timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                           FOREIGN KEY (operation_id) REFERENCES operations(id)
    );


-- Table pour stocker les TTL calculés en fonction des métriques
CREATE TABLE IF NOT EXISTS ttl_calculations (
                                                id INTEGER PRIMARY KEY,
                                                operation_id INTEGER,
                                                ttl REAL,
                                                calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                                FOREIGN KEY (operation_id) REFERENCES operations(id)
    );
