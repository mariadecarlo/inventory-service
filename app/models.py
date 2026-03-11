from sqlalchemy import Column, Integer, String, DateTime
from .database import Base  # importa la classe Base da cui erediteranno tutte le tabelle

# Definizione della tabella "inventory"
class Inventory(Base):
    __tablename__ = "inventory"  # nome della tabella nel database

    # Colonna ID:
    # - Integer: tipo intero
    # - primary_key=True: chiave primaria, unica per ogni record
    # - index=True: crea un indice per velocizzare le query su questa colonna
    id = Column(Integer, primary_key=True, index=True)

    # Colonna productid:
    # - String: tipo testo
    # - index=True: crea un indice per velocizzare le query su productid
    # - nullable=False: obbligatorio, non può essere vuoto
    productid = Column(String, index=True, nullable=False)

    # Colonna quantity:
    # - Integer: tipo intero
    # - nullable=False: obbligatorio
    quantity = Column(Integer, nullable=False)

    # Colonna timestamp:
    # - DateTime: tipo data/ora
    # - index=True: utile per query con intervalli temporali
    # - nullable=False: obbligatorio
    timestamp = Column(DateTime, index=True, nullable=False)