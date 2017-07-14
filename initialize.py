import os

commands = [
    "sqlite3 database.db < schema.sql"
]

for c in commands:
    os.system(c)
