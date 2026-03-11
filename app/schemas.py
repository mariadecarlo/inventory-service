from pydantic import BaseModel, Field
from datetime import datetime

# Schema per la validazione dei dati in ingresso (POST /inventory/update)
class InventoryItem(BaseModel):
    # productid: obbligatorio, almeno 1 carattere
    productid: str = Field(..., min_length=1)
    
    # quantity: obbligatorio, deve essere >= 0
    quantity: int = Field(..., ge=0)
    
    # timestamp: obbligatorio, tipo datetime (ISO 8601)
    timestamp: datetime


# Schema per la risposta dei dati (GET /inventory/query)
class InventoryResponse(BaseModel):
    id: int                 # id generato automaticamente dal DB
    productid: str
    quantity: int
    timestamp: datetime

    class Config:
        # permette a Pydantic di leggere direttamente gli oggetti SQLAlchemy
        # prima si usava 'orm_mode', qui 'from_attributes' fa lo stesso
        from_attributes = True