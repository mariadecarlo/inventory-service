import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",                                # legge la variabile d'ambiente DATABASE_URL
    "postgresql://postgres:postgres@db:5432/inventorydb"  # se non esiste, usa questo default
)