from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional,Literal

# --------- ENTRADA ---------

class ChatCreate(BaseModel):
    title: str = Field(..., min_length=1)
    user_id: int


# --------- RESPUESTA ---------

class ChatResponse(BaseModel):
    chat_id: int
    title: str
    fk_user_id: int
    creation_date: datetime

    class Config:
        from_attributes = True


class MessageCreate(BaseModel):
    chat_id: int
    role: Literal["user", "assistant", "system"]
    content: str = Field(..., min_length=1)


# --------- RESPUESTA ---------

class MessageResponse(BaseModel):
    message_id: int
    fk_chat_id: int
    role: str
    content: str
    sent_date: datetime

    class Config:
        from_attributes = True




# --------- ENTRADA ---------

class DocumentCreate(BaseModel):
    file_name: str
    file_route: str
    user_id: int


# --------- RESPUESTA ---------

class DocumentResponse(BaseModel):
    document_id: int
    file_name: str
    file_route: str
    fk_user_id: int
    load_date: datetime

    class Config:
        from_attributes = True
