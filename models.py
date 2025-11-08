#Este archivo contendrá los modelos de datos que recibirá el servidor

from pydantic import BaseModel

class Query(BaseModel):
    mensaje: str