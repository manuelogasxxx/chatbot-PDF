#for 
from app.services.pdf_loader import get_text_from_pdf
from app.services.chunker import create_chunks
from app.services.embedder import create_embeddings
from app.services.chroma import save_in_chroma

pages = get_text_from_pdf("ejemplo.pdf")
chunks = create_chunks(pages,1000,200)
embed = create_embeddings(chunks)
coleccion = save_in_chroma(embed)
#The search is not done yet