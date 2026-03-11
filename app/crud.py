from sqlalchemy.orm import Session
from .models import Inventory
from .schemas import InventoryItem


# Funzione per inserire più record di inventario nel database
def insert_inventory_items(db: Session, items: list[InventoryItem]):
    records = []  # lista che conterrà gli oggetti Inventory da inserire

    for item in items:
        # Creiamo un oggetto Inventory per ogni item ricevuto
        record = Inventory(
            productid=item.productid,
            quantity=item.quantity,
            timestamp=item.timestamp
        )
        records.append(record)  # aggiungiamo alla lista

    # Aggiunge tutti i record alla sessione DB
    db.add_all(records)
    db.commit()  # salva definitivamente nel database

    return records  # ritorna i record inseriti


# Funzione per fare query filtrate sull'inventario
def query_inventory(db: Session, productid: str, start=None, end=None):
    # partiamo filtrando per productid
    query = db.query(Inventory).filter(Inventory.productid == productid)

    # se c'è start timestamp, filtriamo per record >= start
    if start:
        query = query.filter(Inventory.timestamp >= start)

    # se c'è end timestamp, filtriamo per record <= end
    if end:
        query = query.filter(Inventory.timestamp <= end)

    # ordina i record per timestamp crescente e restituisce tutti i risultati
    return query.order_by(Inventory.timestamp.asc()).all()