#this file contais http urls for the API
import os #manage filesystem
from fastapi import APIRouter, File, UploadFile,HTTPException
from app.models import Query #Class models for the API
from app.services.pdf_loader import get_text_from_pdf_pymupdf4llm
from app.services.chunker import create_chunks
from app.services.embedder import create_embeddings
from app.services.chroma import save_in_chroma
from app.db.session import SessionLocal
from app.database import get_db
from app.db.models import Chat,Message,User,UserRegister
from fastapi import APIRouter, Depends
from app.db.schemas.chats import (ChatCreate,ChatResponse,MessageCreate,MessageResponse,DocumentCreate,DocumentResponse)
from sqlalchemy.orm import Session
from typing import List
from app.core.security import create_access_token,verify_password,hash_password
router = APIRouter()
'''
#DB conection
def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()   # 👈 commit aquí
    except:
        db.rollback()
        raise
    finally:
        db.close()
'''

#custom DIR, make it if doesnt exist
UPLOAD_DIR = "uploads/pdfs"
os.makedirs(UPLOAD_DIR,exist_ok=True)


#rutas para el login
@router.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    # 1. Buscar al usuario por nombre
    user = db.query(User).filter(User.username == username).first()

    # 2. Verificar existencia y validar contraseña
    if not user or not verify_password(password, user.password):
        raise HTTPException(
            status_code=401, 
            detail="Usuario o contraseña incorrectos"
        )

    # 3. Generar token
    token = create_access_token({"sub": str(user.user_id)})
    return {"access_token": token, "token_type": "bearer"}


#crear usuario:
@router.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    hashed_pwd = hash_password(user.password)

    new_user = User(
        username=user.username,
        password=hashed_pwd
    )

    db.add(new_user)
    db.commit()

    return {"message": "Usuario creado exitosamente"}

#Api routes (somo connections depends on db)
@router.get("/")
async def index():
    return {"mensaje": "index page1"}



#para recibir Queries del cliente
@router.post("/query")
async def recibir_datos(data: Query):
    return {"respuesta":f"desde el servidor: {data.mensaje}"}
      

#send files from the client side and store it inside a custom folder
@router.post("/PDF1")
async def create_upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR,file.filename)
    with open(file_path,"wb") as f:
        f.write(await file.read())
    #doesnt handle errors (check that)
    pages = get_text_from_pdf_pymupdf4llm("uploads/pdfs/"+file.filename)
    chunks = create_chunks(pages,1000,200)
    embed = create_embeddings(chunks)
    coleccion = save_in_chroma(embed)
    
    return {"status":"ok","saved_as":file_path}

#crud chats
#@router.post("/chats")
@router.post("/chats", response_model=ChatResponse)
def create_chat(chat_data: ChatCreate, db: Session = Depends(get_db)):
    chat = Chat(
        title=chat_data.title,
        fk_user_id=chat_data.user_id
    )
    db.add(chat)
    db.flush()      # fuerza error FK aquí
    db.refresh(chat)
    return chat

@router.delete("/chats/{chat_id}", status_code=204)
def delete_chat(chat_id: int, db: Session = Depends(get_db)):
    chat = db.get(Chat, chat_id)

    if not chat:
        raise HTTPException(
            status_code=404,
            detail="Chat no encontrado"
        )

    db.delete(chat)
    return


#CRUD Mensajes

@router.post("/messages", response_model=MessageResponse)
def create_message(
    message_data: MessageCreate,
    db: Session = Depends(get_db)
):
    chat = db.get(Chat, message_data.chat_id)
    if not chat:
        raise HTTPException(
            status_code=404,
            detail="Chat no existe"
        )

    message = Message(
        fk_chat_id=message_data.chat_id,
        role=message_data.role,
        content=message_data.content
    )

    db.add(message)
    db.flush()
    db.refresh(message)
    return message

@router.get(
    "/chats/{chat_id}/messages",
    response_model=List[MessageResponse]
)
def get_chat_messages(chat_id: int, db: Session = Depends(get_db)):
    chat = db.get(Chat, chat_id)

    if not chat:
        raise HTTPException(
            status_code=404,
            detail="Chat no encontrado"
        )

    return chat.messages



#crud de documentos
@router.post("/documents", response_model=DocumentResponse)
def create_document(
    message_data: DocumentCreate,
    db: Session = Depends(get_db)
):
    chat = db.get(Chat, message_data.chat_id)
    if not chat:
        raise HTTPException(
            status_code=404,
            detail="Chat no existe"
        )

    message = Message(
        fk_chat_id=message_data.chat_id,
        role=message_data.role,
        content=message_data.content
    )

    db.add(message)
    db.flush()
    db.refresh(message)
    return message