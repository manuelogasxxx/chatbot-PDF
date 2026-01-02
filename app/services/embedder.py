from typing import List, Dict
from fastembed import TextEmbedding
import chromadb

#load the embedder model, this coulb be change anytime
embedder = TextEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")




def create_embeddings(chunks: List[Dict]) -> List[Dict]:
    #print(f"⚙️ Cargando modelo FastEmbed: {model_name}...")
    
    # 1. Inicialización del modelo
    # FastEmbed descarga automáticamente la versión cuantizada (ONNX) del modelo.
    # threads=None usa todos los cores disponibles por defecto.
    #model = TextEmbedding(model_name=model_name)
    
    # Extraer textos
    textos = [c['page_content'] for c in chunks]
    
    print("⚙️ Generando vectores (Stream)...")
    
    # 2. Generación de Embeddings
    # IMPORTANTE: model.embed() devuelve un GENERADOR, no una lista inmediata.
    # Esto ahorra mucha memoria RAM.
    embeddings_generator = embedder.embed(textos)
    
    datos_vectorizados = []
    
    # 3. Iteración simultánea (Zip)
    # Usamos zip para recorrer la lista de chunks original y el generador de vectores al mismo tiempo.
    for i, (chunk, vector) in enumerate(zip(chunks, embeddings_generator)):
        nuevo_chunk = chunk.copy()
        
        # El vector viene como numpy array, lo convertimos a lista para JSON/DB
        nuevo_chunk['vector'] = vector.tolist()
        
        # Generar ID único basado en la fuente y el índice
        # Usamos .get para evitar errores si 'metadata' no tiene 'source'
        source = chunk['metadata'].get('source', 'unknown')
        nuevo_chunk['id'] = f"{source}_{i}"
        
        datos_vectorizados.append(nuevo_chunk)
        
    # Verificación de seguridad por si la lista está vacía
    if datos_vectorizados:
        dim = len(datos_vectorizados[0]['vector'])
        print(f"✅ Vectorización completada. {len(datos_vectorizados)} chunks procesados.")
        print(f"📊 Dimensión del vector: {dim}")
    else:
        print("⚠️ No se generaron vectores (lista de chunks vacía).")

    return datos_vectorizados

def load_collection(path_db="chromaDB", collection_name="myDocuments"):
    client = chromadb.PersistentClient(path=path_db)
    collection = client.get_collection(name=collection_name)
    return collection
#this function embedd a query and its part of the main RAG
#collection correspond to the return value of chroma.py function
def buscar_similares(archivo,collection, texto_consulta, embedding_model, k=5):
    # FastEmbeddings → generator → list
    query_embedding = next(embedding_model.embed(texto_consulta))

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        where={"source": archivo}
    )

    return results

