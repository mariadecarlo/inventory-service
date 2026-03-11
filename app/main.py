from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import time

from .database import Base, engine, get_db  # Base per i modelli, engine per DB, get_db per sessioni
from . import schemas, crud  # importa schemi Pydantic e funzioni CRUD

# Crea l'app FastAPI
app = FastAPI()


# Evento di startup: viene eseguito all'avvio del server
@app.on_event("startup")
def startup():
    """
    Creazione delle tabelle se non esistono e retry per la connessione al DB
    (utile quando il DB è in Docker e potrebbe non essere pronto subito)
    """
    for i in range(10):  # prova fino a 10 volte
        try:
            Base.metadata.create_all(bind=engine)  # crea tutte le tabelle del DB
            print("Database connected!")
            break  # se va a buon fine, esce dal ciclo
        except Exception:
            print("Database not ready, retrying...")
            time.sleep(2)  # aspetta 2 secondi prima di riprovare


# Endpoint POST /inventory/update
@app.post("/inventory/update")
def update_inventory(
    items: List[schemas.InventoryItem],  # lista di oggetti validati da Pydantic
    db: Session = Depends(get_db)       # dipendenza FastAPI per ottenere la sessione DB
):
    try:
        records = crud.insert_inventory_items(db, items)  # inserisce i record nel DB
        return {"inserted": len(records)}                # ritorna il numero di record inseriti
    except Exception:
        # se qualcosa va storto, ritorna errore 500
        raise HTTPException(status_code=500, detail="Database write failed")


# Endpoint GET /inventory/query
@app.get("/inventory/query", response_model=List[schemas.InventoryResponse])
def query_inventory(
    productid: str,  # filtro obbligatorio per il prodotto
    starttimestamp: Optional[datetime] = Query(None),  # filtro opzionale inizio
    endtimestamp: Optional[datetime] = Query(None),    # filtro opzionale fine
    db: Session = Depends(get_db)                      # sessione DB
):
    try:
        records = crud.query_inventory(
            db,
            productid,
            starttimestamp,
            endtimestamp
        )
        return records  # ritorna lista di record serializzati in JSON
    except Exception:
        # se qualcosa va storto, ritorna errore 500
        raise HTTPException(status_code=500, detail="Database query failed")