"""
This file contains the code for load text from a PDF trying to emulate
langchain text extractor.
Next changes:
    *PymuPDF4LLM for extract tables and images in markdown
    *OCRTESSERACT for scanned PDFs
"""
import pymupdf.layout
import fitz #pymuPDF
import pymupdf4llm

import re
#this function cleans text using basic regex
#anoher clean clauses could be used
def clean_text(raw_text):
    if not raw_text:
        return ""
    #words minced by end of line
    clean_text = re.sub(r'-\n','',raw_text)
    #replace line jumps for a simple espace
    clean_text = clean_text.replace('\n',' ')
    #delete multiple "spaces"
    clean_text = re.sub(r'\s+', ' ', clean_text)
    return clean_text.strip()


#this function emulate langchain load function
#at first this function only handle pdfs not OCR is used
def get_text_from_pdf(route):
    try:
        
        doc = fitz.open(route)
        data = []
        doc_length = len(doc)
        for i, page in enumerate(doc):
            #extract plain text
            raw_content = page.get_text()
            clean_content = raw_content#clean_text(raw_content)
            
            if clean_content:
                #this metadate may change for better seek functions in the embedding part
                metadata ={
                    "source": route,
                    "page": i,
                    "total_pages":doc_length
                }
                data.append({
                    "page_content": clean_content,
                    "metadata": metadata
                })
        doc.close()
        return data
        
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")
        return []

def get_text_from_pdf_pymupdf4llm(route):
    doc = None
    try:
        # 1. Abrimos el documento primero con fitz (PyMuPDF)
        doc = fitz.open(route)
        doc_length = len(doc)
        
        # 2. Le pasamos el objeto 'doc' abierto a PyMuPDF4LLM
        # Esto elimina la posibilidad de que PyMuPDF4LLM tenga problemas 
        # al abrir el archivo por sí mismo.
        data_chunks = pymupdf4llm.to_markdown(
            doc=doc,
            page_chunks=True
        )
        
        # El resto del código para transformar el formato sigue igual...
        data = []
        for chunk in data_chunks:
            clean_content = chunk['text'] 
            
            if clean_content:
                # Aseguramos que los metadatos de PyMuPDF4LLM existan
                metadata = {
                    # PyMuPDF4LLM puede no incluir 'source' si le pasas el objeto abierto.
                    # Usamos la 'route' original
                    "source": route, 
                    "page": chunk['metadata'].get('page', 0),
                    "total_pages": doc_length 
                }
                
                data.append({
                    "page_content": clean_content,
                    "metadata": metadata
                })
        
        # 3. Cerramos el documento
        doc.close()
        return data
        
    except Exception as e:
        print(f"Error al procesar el archivo con PyMuPDF4LLM: {e}")
        # Asegurarse de cerrar el doc si se abrió antes del error
        if doc:
            doc.close()
        return []
     
#verification
'''
ruta = "ejemplo.pdf"
data_pdf=get_text_from_pdf_pymupdf4llm(ruta)
if data_pdf:
    print(f"--- Página {data_pdf[0]['metadata']['page']} ---")
    # Imprimimos los primeros 200 caracteres para ver la diferencia
    print(data_pdf[0]['page_content'])
else:
    print("No se encontraron datos o el PDF está vacío/es una imagen escaneada.")
'''
