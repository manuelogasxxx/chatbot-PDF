from fastembed import TextEmbedding

#load the embedder model
embedder = TextEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

def embed_chunks(chunks):
    return [embedder.embed(doc)[0] for doc in chunks]




