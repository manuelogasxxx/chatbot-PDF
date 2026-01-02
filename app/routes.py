#this file contais http urls for the API
import os #manage filesystem
from fastapi import APIRouter, File, UploadFile
from app.models import Query #Class models for the API
from app.services.pdf_loader import get_text_from_pdf_pymupdf4llm
from app.services.chunker import create_chunks
from app.services.embedder import create_embeddings
from app.services.chroma import save_in_chroma
router = APIRouter()

#custom DIR, make it if doesnt exist
UPLOAD_DIR = "uploads/pdfs"
os.makedirs(UPLOAD_DIR,exist_ok=True)

#Api routes
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