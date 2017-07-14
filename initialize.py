import os

commands = [
    "sqlite3 db.db < schema.sql"
]

for c in commands:
    os.system(c)
