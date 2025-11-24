#this file contains the code for 
import fitz #pymuPDF
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
            
#verificion
ruta = "ejemplo.pdf"
data_pdf=get_text_from_pdf(ruta)
if data_pdf:
    print(f"--- Página {data_pdf[0]['metadata']['page']} ---")
    # Imprimimos los primeros 200 caracteres para ver la diferencia
    print(data_pdf[0]['page_content'])
else:
    print("No se encontraron datos o el PDF está vacío/es una imagen escaneada.")

#The file conversion is quicl