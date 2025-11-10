import os
from docx import Document
import PyPDF2
import pypandoc

def abrir_archivo(ruta):
    # Verificar que el archivo exista
    if not os.path.exists(ruta):
        print("❌ El archivo no existe.")
        return

    # Obtener la extensión
    _, extension = os.path.splitext(ruta)
    extension = extension.lower()

    try:
        if extension == ".txt":
            # Leer texto plano
            with open(ruta, "r", encoding="utf-8") as f:
                contenido = f.read()
        
        elif extension == ".docx":
            # Leer documentos Word
            doc = Document(ruta)
            contenido = "\n".join([p.text for p in doc.paragraphs])
        
        elif extension == ".pdf":
            # Leer archivos PDF
            with open(ruta, "rb") as f:
                lector = PyPDF2.PdfReader(f)
                contenido = ""
                for pagina in lector.pages:
                    contenido += pagina.extract_text() + "\n"
        
        elif extension == ".rtf":
            # Convertir RTF a texto usando pypandoc
            contenido = pypandoc.convert_text(open(ruta, encoding="utf-8").read(), 'plain', format='rtf')

        else:
            print("⚠️ Tipo de archivo no soportado.")
            return

        print("\n📄 CONTENIDO DEL ARCHIVO:\n")
        print(contenido)

    except Exception as e:
        print(f"❌ Error al abrir el archivo: {e}")

# ------------------------------
# Ejemplo de uso
# ------------------------------
ruta = input("Ingrese la ruta del archivo: ")
abrir_archivo(ruta)
