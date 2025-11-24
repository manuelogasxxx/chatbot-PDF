#this file will save embeddings inside a chroma folder

import chromadb

def save_in_chroma(datos_vectorizados: list, path_db: str = "chromaDB", collection_name: str = "myDocuments"):
    """
    Recibe la lista de chunks con vectores y los guarda en ChromaDB de forma persistente.
    """
    if not datos_vectorizados:
        print("⚠️ No hay datos para guardar.")
        return

    print(f"💾 Conectando a ChromaDB en: {path_db}...")
    
    # 1. Crear cliente persistente (para que los datos se guarden en disco y no solo en RAM)
    client = chromadb.PersistentClient(path=path_db)
    
    # 2. Obtener o crear la colección
    # Una colección es como una "tabla" en SQL.
    collection = client.get_or_create_collection(name=collection_name)
    
    print(f"📦 Preparando {len(datos_vectorizados)} documentos para inserción...")

    # 3. Preparar los datos en listas separadas (Formato Columnar)
    # Chroma espera: ids=[...], embeddings=[...], documents=[...], metadatas=[...]
    ids = [item['id'] for item in datos_vectorizados]
    embeddings = [item['vector'] for item in datos_vectorizados]
    documents = [item['page_content'] for item in datos_vectorizados]
    metadatas = [item['metadata'] for item in datos_vectorizados]

    # 4. Insertar en lotes (Batch)
    # .add lanzará error si los IDs ya existen. Usa .upsert si quieres sobrescribir.
    try:
        collection.upsert(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas
        )
        print(f"✅ Éxito: {len(ids)} documentos guardados en la colección '{collection_name}'.")
    except Exception as e:
        print(f"❌ Error al guardar en Chroma: {e}")

    return collection # Retornamos la colección por si queremos hacer consultas inmediatas