#this file contains functions for chunking data
#an easy way is implemented but more complex may be added
import re
from typing import List, Dict, Any

#this function return a list of strings of chunk_size+chunk_overlap 
def dividir_en_chunks(texto, chunk_size=1000, chunk_overlap=200):
    """
    Divide un texto largo en fragmentos más pequeños respetando palabras completas
    y manteniendo un contexto compartido (overlap).
    """
    if not texto:
        return []
    
    # 1. Dividimos el texto en palabras para no cortar a mitad de una palabra
    palabras = texto.split(' ')
    chunks = []
    
    current_chunk = []
    current_length = 0
    
    for palabra in palabras:
        # Calculamos longitud de la palabra + 1 espacio
        len_palabra = len(palabra) + 1 
        
        # 2. Si agregar la palabra no supera el límite, la agregamos
        if current_length + len_palabra <= chunk_size:
            current_chunk.append(palabra)
            current_length += len_palabra
        
        # 3. Si supera el límite, cerramos el chunk actual
        else:
            # Unimos las palabras y guardamos el chunk
            chunks.append(" ".join(current_chunk))
            
            # --- LÓGICA DE OVERLAP ---
            # Para el nuevo chunk, tomamos las últimas palabras del chunk anterior
            # hasta llenar el tamaño del overlap.
            overlap_buffer = []
            overlap_len = 0
            
            # Recorremos el chunk actual hacia atrás
            for p in reversed(current_chunk):
                if overlap_len + len(p) + 1 <= chunk_overlap:
                    overlap_buffer.insert(0, p) # Insertamos al principio
                    overlap_len += len(p) + 1
                else:
                    break
            
            # Iniciamos el nuevo chunk con el overlap + la palabra que desbordó
            current_chunk = list(overlap_buffer)
            current_chunk.append(palabra)
            current_length = overlap_len + len_palabra

    # 4. Agregar el último fragmento si quedó algo pendiente
    if current_chunk:
        chunks.append(" ".join(current_chunk))
        
    return chunks



def division_recursiva_manual(texto, chunk_size=1000, chunk_overlap=200):
    if not texto:
        return []

    # Lista de separadores en orden de prioridad (igual que LangChain)
    separadores = ["\n\n", "\n", " ", ""]
    
    # 1. Determinar qué separador usar
    separador_final = ""
    for sep in separadores:
        if sep == "":
            separador_final = ""
            break
        if sep in texto:
            separador_final = sep
            break
            
    # 2. Dividir el texto usando ese separador
    if separador_final:
        bloques = texto.split(separador_final)
    else:
        bloques = list(texto) # Convertir string a lista de caracteres

    # 3. Reconstruir chunks fusionando bloques hasta alcanzar el tamaño
    chunks_finales = []
    chunk_actual = []
    len_actual = 0
    
    for bloque in bloques:
        len_bloque = len(bloque) + len(separador_final)
        
        if len_actual + len_bloque > chunk_size:
            # El chunk está lleno, lo guardamos
            texto_unido = separador_final.join(chunk_actual)
            if texto_unido.strip():
                chunks_finales.append(texto_unido)
            
            # --- Lógica de Overlap simplificada ---
            # Mantenemos algunos bloques del final para el siguiente chunk
            # (Nota: LangChain tiene una lógica de overlap más compleja aquí, 
            #  pero esto emula el comportamiento básico)
            while len_actual > chunk_overlap and chunk_actual:
                removido = chunk_actual.pop(0)
                len_actual -= (len(removido) + len(separador_final))
            
        chunk_actual.append(bloque)
        len_actual += len_bloque

    # Guardar lo que sobró
    if chunk_actual:
        chunks_finales.append(separador_final.join(chunk_actual))

    return chunks_finales

#finally we iterate over a list of pages 

def _split_recursivo(texto: str, chunk_size: int, chunk_overlap: int) -> List[str]:
    """
    Lógica interna: Divide texto intentando respetar párrafos y oraciones.
    """
    separadores = ["\n\n", ". ", " ", ""] # Prioridad de corte
    separador_usado = ""
    
    # Buscar el mejor separador
    for sep in separadores:
        if sep in texto:
            separador_usado = sep
            break
            
    bloques = texto.split(separador_usado) if separador_usado else list(texto)
    
    chunks = []
    chunk_actual = []
    len_actual = 0
    
    for bloque in bloques:
        # Recuperamos el separador para el conteo real de caracteres
        len_bloque = len(bloque) + len(separador_usado)
        
        if len_actual + len_bloque > chunk_size:
            # Guardar chunk actual
            texto_unido = separador_usado.join(chunk_actual)
            if texto_unido:
                chunks.append(texto_unido)
            
            # Gestionar Overlap (mantener el final del chunk anterior)
            while len_actual > chunk_overlap and chunk_actual:
                removido = chunk_actual.pop(0)
                len_actual -= (len(removido) + len(separador_usado))
        
        chunk_actual.append(bloque)
        len_actual += len_bloque
        
    if chunk_actual:
        chunks.append(separador_usado.join(chunk_actual))
        
    return chunks

#return a List of dictionaries, each one contains a document page and its metadata
#return a List[Dict]
def create_chunks(documents: List[Dict], chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Dict]:
    all_chunks = []
    
    for doc in documents:
        diveded_text = _split_recursivo(doc['page_content'], chunk_size, chunk_overlap)
        
        for fragment in diveded_text:
            all_chunks.append({
                "page_content": fragment,
                "metadata": doc['metadata'] # Insert metadata's page in each chunk
            })
            
    print(f"✅ Chunking completed: {len(all_chunks)} chunks generated.")
    return all_chunks