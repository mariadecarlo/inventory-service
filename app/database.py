from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import DATABASE_URL  # importa l'URL del database da config.py

# Crea l'engine SQLAlchemy, cioè il "motore" per connettersi al DB
engine = create_engine(DATABASE_URL)

# Crea un "sessionmaker", che genera sessioni per interagire con il DB
# - autocommit=False: le modifiche non vengono salvate automaticamente
# - autoflush=False: non invia automaticamente i cambiamenti al DB fino al commit
# - bind=engine: collega le sessioni all'engine sopra
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base è la classe da cui erediteranno tutti i modelli (tabelle)
Base = declarative_base()

# Funzione helper per ottenere una sessione DB per ogni richiesta FastAPI
# yield serve per usare la sessione come "context manager", cioè chiude automaticamente alla fine
def get_db():
    db = SessionLocal()  # crea una nuova sessione
    try:
        yield db           # fornisce la sessione al codice che la richiede
    finally:
        db.close()         # chiude sempre la sessione al termine dell'uso