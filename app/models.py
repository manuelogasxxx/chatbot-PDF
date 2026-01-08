#Este archivo contendrá los modelos de datos que recibirá el servidor

from typing import Optional
from pydantic import BaseModel

class Query(BaseModel):
    mensaje: str
    
    


class UserRegister(BaseModel):
    username: str
    password: str

class QueryRequest(BaseModel):
    user_id: int
    document_id: int
    query_mode: str  # "semantic", "translation", "tables"
    
    # Entradas opcionales dependiendo del modo
    text_input: Optional[str] = None
    page_number: Optional[int] = None