import sqlite3

# Connection to the database
db = sqlite3.connect("metrics.db", detect_types=sqlite3.PARSE_DECLTYPES)
db.row_factory = sqlite3.Row  # Return rows as dictionaries