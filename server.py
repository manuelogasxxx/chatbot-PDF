#Este archivo ejecuta el servidor que procesará las solicitudes de la web
#podrá ser ejecutado en localhost o en una computadora diferente
#el cliente manda PDF y/o mensajes al backend y este responde con JSON .

#Retos: -> Tener memoria (actualizarla y restaurarla)
#       -> Arquitectura que minimice la generación de texto

#pip install flask flask-cors pymupdf
#pip install fastapi uviconrn+


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import fitz  # PyMuPDF para leer PDFs

app = FastAPI() #creación del servidor
#CORSMiddleware(app)  # Permite que una página web externa acceda a la API



@app.get("/")
async def index():
    return {"mensaje": "index page1"}



#para mandar Queries



#esta




