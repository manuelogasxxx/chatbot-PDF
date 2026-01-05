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
from app.core.dependencies import get_current_user
from app.db.models import Chat,Message,User,UserRegister
from fastapi import APIRouter, Depends
from app.db.schemas.chats import (ChatCreate,ChatResponse,MessageCreate,MessageResponse,DocumentCreate,DocumentResponse)
from sqlalchemy.orm import Session
from typing import List
from app.core.security import create_access_token,verify_password,hash_password
from fastapi.security import OAuth2PasswordRequestForm
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
async def login(
    # Cambia tu esquema Pydantic por esta dependencia
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    # Ahora accedes a los datos así:
    user = db.query(User).filter(User.username == form_data.username).first()
    
    # ... tu lógica de validación de contraseña ...
    
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    # Generar token (asegúrate de devolver 'access_token' y 'token_type')
    token = create_access_token(data={"sub": str(user.user_id)})#user.username
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
def create_chat(
    chat_data: ChatCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # <--- Inyección de seguridad
):
    chat = Chat(
        title=chat_data.title,
        fk_user_id=current_user.user_id # Usamos el ID del token, no del body
    )
    
    try:
        db.add(chat)
        #db.flush() 
        db.commit() # No olvides el commit para persistir
        db.refresh(chat)
        return chat
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error al crear el chat")

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

@router.get("/chats1")
def get_user_chats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Filtramos solo los chats de este usuario
    return db.query(Chat).filter(Chat.fk_user_id == current_user.user_id).all()
#CRUD Mensajes

@router.post("/messages", response_model=MessageResponse)
def create_message(
    message_data: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verificar que el chat pertenezca al usuario actual
    chat = db.get(Chat, message_data.chat_id)
    if not chat:
        raise HTTPException(
            status_code=404,
            detail="Chat no existe"
        )
    
    # Verificar que el chat pertenezca al usuario autenticado
    if chat.fk_user_id != current_user.user_id:
        raise HTTPException(
            status_code=403,
            detail="No tienes permiso para enviar mensajes a este chat"
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
def get_chat_messages(
    chat_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verificar que el chat pertenezca al usuario actual
    chat = db.get(Chat, chat_id)

    if not chat:
        raise HTTPException(
            status_code=404,
            detail="Chat no encontrado"
        )
    
    # Verificar que el chat pertenezca al usuario autenticado
    if chat.fk_user_id != current_user.user_id:
        raise HTTPException(
            status_code=403,
            detail="No tienes permiso para acceder a este chat"
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