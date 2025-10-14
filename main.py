#pruebas de extracción de texto
#es necesario comprobar si es texto o imagen

import fitz #PymuPDF (se instala)
import re #regular expresions
import nltk #natutal language tool kit (se instala)
import spacy
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
import string



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





#Acciones principales
prueba = ProcesamientoDeTexto()
doc = fitz.open("ejemplo.pdf")
#print(doc.get_page_text(0))
text=prueba.preprocess(doc.get_page_text(0))
print(text)
doc.close()