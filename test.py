#for 
from app.services.pdf_loader import get_text_from_pdf
from app.services.chunker import make_chunks
from app.services.embedder import generar_embeddings
from app.services.chroma import save_in_chroma

pages = get_text_from_pdf("ejemplo.pdf")
chunks = make_chunks(pages,1000,200)
embed = generar_embeddings(chunks)
coleccion = save_in_chroma(embed)
#falta hacer la busqueda