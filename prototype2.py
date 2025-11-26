#this is just a fast prototype using langchain wich is easy but adds overhead  
#Chunks
from langchain_text_splitters import RecursiveCharacterTextSplitter
#Load PDF
from langchain_community.document_loaders import PyMuPDFLoader
#LLM models for execution
# from langchain_community.llms import Ollama
from langchain_ollama import OllamaLLM
#For Embeddings
from langchain_community.embeddings import FastEmbedEmbeddings
#Vectorial DB (FAISS is faster)
from langchain_community.vectorstores import Chroma
from langchain_community.vectorstores import FAISS
#promp template
from langchain_core.prompts import PromptTemplate  
#get an answer from the LLM
from langchain_classic.chains import RetrievalQA

llm = OllamaLLM(model="phi3") #The principal LLM choosen is phi3 bc is advantajes

#loads the embedded model all-MiniLM-L6-v2 wich is "fast" and suitable
embed_model = FastEmbedEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

#loads the PDF document and extract the info
loader = PyMuPDFLoader("ejemplo.pdf") #cargar el documento
data_pdf = loader.load()

#chunk_size && chunk_overlap may change in order to experiment
text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000,chunk_overlap=500)

#genera una lista pag a pag con la información del pdf
docs = text_splitter.split_documents(data_pdf)

#parte adicional (vectorizacion de chunks)
#vs = Chroma.from_documents(
#    documents=docs,
#    embedding=embed_model,
#    persist_directory="chroma_db_dir",
#    collection_name="archivo"
#)
#store a vectorial DB of the document and store it in ¡RAM!
vectorstore = FAISS.from_documents(docs,embed_model)


retriever = vectorstore.as_retriever(search_kwargs={'k':3})

query = "¿de que trata el texto?"

# 2. Usa el retriever para obtener solo los documentos más relevantes
#    El método get_relevant_documents devuelve una lista de objetos Document
relevant_chunks = retriever.invoke(query)

# 3. Imprime solo el contenido (page_content) de cada chunk encontrado
print(f"Chunks relevantes para la consulta: '{query}'\n")

for i, chunk in enumerate(relevant_chunks):
    print(f"--- Chunk {i+1} ---")
    print(chunk.page_content)
    # Puedes incluir metadata si te interesa saber de qué página proviene, etc.
    # print(chunk.metadata) 
    print("-------------------\n")