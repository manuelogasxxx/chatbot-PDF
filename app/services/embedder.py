from typing import List, Dict
from fastembed import TextEmbedding

#load the embedder model, this coulb be change anytime
embedder = TextEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

def embed_chunks(chunks):
    return [embedder.embed(doc)[0] for doc in chunks]



#finally each embedding is stored in chroma

def generar_embeddings(chunks: List[Dict]) -> List[Dict]:
    """
    Enriquece los chunks usando FastEmbed (ligero, rápido, sin PyTorch pesado).
    """
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

#this function embedd a query.