#This file will execute the server
#for dev use: uvicorn server:app --reload
#CORS allows this server to catch request from local networks and localhost


#Retos: -> Tener memoria (actualizarla y restaurarla)
#       -> Arquitectura que minimice la generación de texto

#pip install flask flask-cors pymupdf
#pip install fastapi uviconrn+


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router #separate routes from the server

app = FastAPI() #server creation
app.include_router(router) #routes from a separate file

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




