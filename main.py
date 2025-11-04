#pruebas de extracción de texto
#es necesario comprobar si es texto o imagen
import fitz #PymuPDF (se instala)
import re #regular expresions
import nltk #natutal language tool kit (se instala)
import spacy
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
import string

#hacer chunks
from langchain_text_splitters import RecursiveCharacterTextSplitter
#Cargar PDF
from langchain_community.document_loaders import PyMuPDFLoader
#contiene los modelos a ejecutar
# from langchain_community.llms import Ollama
from langchain_ollama import OllamaLLM
#para los embeddings (se puede cambiar)
from langchain_community.embeddings import FastEmbedEmbeddings
#para la base de datos vectorial (FAISS es más rápida)
from langchain_community.vectorstores import Chroma
from langchain_community.vectorstores import FAISS

from langchain_core.prompts import PromptTemplate  

from langchain_classic.chains import RetrievalQA



llm = OllamaLLM(model="phi3") #el modelo principal para las pruebas es phi3


#constantes 
#stop_words_spanish = set(stop)






#función que preprocesa el texto ingresado
#se va a trabajar con inglés y español

#opciones baratas vs complejas
class ProcesamientoDeTexto:
    
    def __init__(self):
        #atributos para regex
        self.stopWordSpanish = set(stopwords.words('spanish'))
        self.stopWordEnglish = set(stopwords.words('english'))
        #atributos para spacy
        try:
            self.spacyIdiomas ={
                "es":spacy.load("es_core_news_sm",disable=['parser','ner']), #español
                "en":spacy.load("en_core_web_sm",disable=['parser','ner'])  #ingles
            }
            
        except OSError:
            raise Exception("Modelo(s) no econtrado(s)")
    
    #alternativa rapida de preprocesamiento
    def regexPreprocess(self,text):
        #se pueden modificar las expresiones regulares
        text= re.sub(r'[^\w\s]',' ',text.lower())
        words = text.split()
        
        filtered = [word for word in words 
                    if word not in self.stopWordEnglish
                    and len(word) > 2 
                    and not word.isdigit()]
        return " ".join(filtered)
        #costo algoritmico O(3n)        

    def preprocess(self,text):
        #headers y footers
        text = re.sub(r'\n\d+\s*\n', '\n', text)  # Números de página solos
        text = re.sub(r'©.*\n', '\n', text)  # Copyright
        text = re.sub(r'ISSN.*\n', '\n', text)  # ISSN
        
        #saltos de linea incorrectos
        text = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', text)

        #se pueden eliminar mas cosas (Probar)

        #caracteres especiales
        text= re.sub(r'[•■♦➢➤]', ' ', text)
        return text.strip()

    #se pueden colocar constraints de longitud del PDF
    def getText(self,path):
        text=[]
        with fitz.open(path) as doc:
            for page in doc:
                text.append(page.get_text("text"))
        return "\n".join(text)
    
    def getText2(self, path, start=0, end=None):
        text = []
        with fitz.open(path) as doc:
            if end is None or end > len(doc):
                end = len(doc)
            for page_num in range(start, end):
                page = doc.load_page(page_num)
                text.append(page.get_text("text"))
        return "\n".join(text)

        
                
#se está haciendo un prototipado rápido




#Acciones principales

embed_model = FastEmbedEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

loader = PyMuPDFLoader("ejemplo.pdf") #cargar el documento

data_pdf = loader.load() #obtener la informacion del pdf
#chunk_size y chunk_overlap pueden modificarse para verfificar el rendimiento

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
vectorstore = FAISS.from_documents(docs,embed_model)

retriever = vectorstore.as_retriever(search_kwargs={'k':3})

custom_prompt_template = """Usa la siguiente información para responder a la pregunta del usuario.
Si no sabes la respuesta, simplemente di que no lo sabes, no intentes inventar una respuesta.

Contexto: {context}
Pregunta: {question}

Solo devuelve la respuesta útil a continuación y nada más y responde siempre en español
Respuesta útil:
"""
prompt = PromptTemplate(template=custom_prompt_template,
                        input_variables=['context', 'question'])


qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True,
    chain_type_kwargs={"prompt": prompt}
)



# 6. Consultar
query = "¿De que habla el modelo propuesto?"

result = qa.invoke({"query": query})

print("Respuesta:", result["result"])
#prueba = ProcesamientoDeTexto()
#doc = fitz.open("ejemplo.pdf")
#print(doc.get_page_text(0))
#text=prueba.getText("ejemplo.pdf")
#print(text)
