#for 
from app.services.pdf_loader import get_text_from_pdf
from app.services.pdf_loader import get_text_from_pdf_pymupdf4llm
from app.services.chunker import create_chunks
from app.services.embedder import create_embeddings
from app.services.embedder import load_collection
from app.services.embedder import buscar_similares

from app.services.chroma import save_in_chroma
from fastembed import TextEmbedding
embedder = TextEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
pages = get_text_from_pdf("uploads/pdfs/ejemplo.pdf")
chunks = create_chunks(pages,1000,200)
embed = create_embeddings(chunks)
coleccion = save_in_chroma(embed)

collection = load_collection(
    path_db="chromaDB",
    collection_name="myDocuments"
)


query = "¿de que trata el documento?"

nombre = "ejemplo.pdf"

results = buscar_similares(
    nombre,
    collection=collection,
    texto_consulta=query,
    embedding_model=embedder,
    k=3
)

for i, doc in enumerate(results["documents"][0]):
    print(f"\n🔹 Resultado {i+1}")
    print(doc)
