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

def get_text_from_pdf_pymupdf4llm(route, document_id):
    doc = None
    try:
        # 1. Abrir documento
        doc = fitz.open(route)
        doc_length = len(doc)
        
        # 2. Extraer Markdown
        data_chunks = pymupdf4llm.to_markdown(doc=doc, page_chunks=True)
        
        data = []
        
        # Usamos enumerate para tener un 'backup' del número de página
        # 'index' empezará en 0, 1, 2...
        for index, chunk in enumerate(data_chunks):
            clean_content = chunk['text'] 
            
            if clean_content:
                # --- CORRECCIÓN DE PÁGINAS ---
                # Intentamos leer el metadato de la librería
                raw_page = chunk['metadata'].get('page')
                
                if raw_page is not None:
                    # Si existe (ej: 0), le sumamos 1 -> Pág 1
                    final_page = raw_page + 1
                else:
                    # Si la librería falló, usamos el índice del bucle -> Pág 1
                    final_page = index + 1
                
                # Construimos el metadato corregido
                metadata = {
                    "source": route, 
                    "page": final_page, # <--- AQUÍ ESTÁ EL VALOR CORREGIDO (1, 2, 3...)
                    "total_pages": doc_length,
                    "document_id": document_id 
                }
                
                data.append({
                    "page_content": clean_content,
                    "metadata": metadata
                })
                
                # Debug para verificar que se arregló
                if index == 0:
                    print(f"✅ Página 1 corregida. Se guardará como: {final_page}")

        doc.close()
        return data
        
    except Exception as e:
        print(f"❌ Error crítico en procesamiento PDF: {e}")
        if doc: doc.close()
        return []


def extract_tables_from_page(file_path: str, page_num: int):
    """
    Usa pymupdf4llm para obtener el markdown de una página específica.
    """
    # Nota: page_num viene base 1 del usuario, PyMuPDF usa base 0
    try:
        # pymupdf4llm.to_markdown devuelve todo el texto formateado.
        # Es excelente detectando tablas.
        markdown_content = pymupdf4llm.to_markdown(
            file_path, 
            pages=[page_num - 1] 
        )
        return markdown_content
    except Exception as e:
        return f"Error leyendo página: {str(e)}"
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
