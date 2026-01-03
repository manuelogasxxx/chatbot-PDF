#Contains classes to validate registers to DB
from pydantic import BaseModel

class ChatCreate(BaseModel):
    title: str
    user_id: int
