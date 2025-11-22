#this file contais http urls for the API
import os
from fastapi import APIRouter, File, UploadFile
from models import Query #Class models for the API
router = APIRouter()

@router.get("/")
async def index():
    return {"mensaje": "index page1"}



#para recibir Queries del cliente
@router.post("/query")
async def recibir_datos(data: Query):
    return {"respuesta":f"desde el servidor: {data.mensaje}"}
      

#send files from the client side and store it inside a define folder
@router.post("/PDF1")
async def create_upload_file(file: UploadFile = File(...)):
    
    return {"filename":file.name}