import os
import json
import numpy as np
from dotenv import load_dotenv
from pypdf import PdfReader
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

CACHE_FILE = "embeddings_cache.json"

def cargar_pdfs(carpeta="data"):
    chunks = []
    for archivo in os.listdir(carpeta):
        if archivo.endswith(".pdf"):
            reader = PdfReader(os.path.join(carpeta, archivo))
            for pagina in reader.pages:
                texto = pagina.extract_text()
                if texto and texto.strip():
                    for i in range(0, len(texto), 500):
                        chunk = texto[i:i+500].strip()
                        if chunk:
                            chunks.append({"texto": chunk, "fuente": archivo})
    return chunks

def get_embedding(texto):
    result = client.models.embed_content(
        model="models/gemini-embedding-001",
        contents=texto
    )
    return result.embeddings[0].values

def cargar_o_generar_embeddings(chunks):
    # Si existe cache, cárgalo
    if os.path.exists(CACHE_FILE):
        print("Cache encontrado, cargando embeddings desde disco...")
        with open(CACHE_FILE, "r") as f:
            cache = json.load(f)
        # Verifica que el cache corresponde a los mismos chunks
        if cache["num_chunks"] == len(chunks):
            return [np.array(e) for e in cache["embeddings"]]
        print("Cache desactualizado, regenerando...")

    # Si no existe cache, genera y guarda
    print("Generando embeddings...")
    embeddings = [get_embedding(c["texto"]) for c in chunks]
    cache = {
        "num_chunks": len(chunks),
        "embeddings": [e for e in embeddings]
    }
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f)
    print("Embeddings guardados en disco")
    return [np.array(e) for e in embeddings]

def buscar_chunks(query, chunks, embeddings, top_k=3):
    query_emb = np.array(get_embedding(query))
    similitudes = []
    for i, emb in enumerate(embeddings):
        similitud = np.dot(query_emb, emb) / (np.linalg.norm(query_emb) * np.linalg.norm(emb))
        similitudes.append((similitud, i))
    similitudes.sort(reverse=True)
    return [chunks[i] for _, i in similitudes[:top_k]]

def responder(pregunta, contexto_chunks):
    contexto = "\n\n".join([f"[{c['fuente']}]: {c['texto']}" for c in contexto_chunks])
    prompt = f"""Eres un asistente técnico de IBM. Responde la pregunta usando SOLO el contexto proporcionado.
Si el contexto no contiene la respuesta, dilo explícitamente.

CONTEXTO:
{contexto}

PREGUNTA: {pregunta}

RESPUESTA:"""
    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt
    )
    return response.text

# MAIN
print("Cargando documentos...")
chunks = cargar_pdfs("data")
print(f"{len(chunks)} chunks generados")

embeddings = cargar_o_generar_embeddings(chunks)

print("\n=== IBM Knowledge Agent ===")
print("Escribe 'salir' para terminar\n")

while True:
    pregunta = input("Tu pregunta: ")
    if pregunta.lower() == "salir":
        break
    if not pregunta.strip():
        continue
    chunks_relevantes = buscar_chunks(pregunta, chunks, embeddings)
    respuesta = responder(pregunta, chunks_relevantes)
    print(f"\nRespuesta: {respuesta}\n")