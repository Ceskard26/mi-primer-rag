
# Mi Primer RAG — IBM Knowledge Agent

RAG (Retrieval-Augmented Generation) construido desde cero sin frameworks como LangChain o LlamaIndex.

El agente responde preguntas en lenguaje natural sobre documentación técnica de IBM, usando únicamente el contenido de los documentos proporcionados como fuente de verdad.

## Cómo funciona

1. **Ingesta** — lee PDFs de la carpeta `data/` y los divide en chunks de 500 caracteres
2. **Embeddings** — convierte cada chunk en un vector numérico usando `gemini-embedding-001`
3. **Retrieval** — ante una pregunta, calcula similitud coseno entre la pregunta y todos los chunks, retorna los 3 más relevantes
4. **Generation** — manda esos chunks como contexto a `gemini-2.5-flash` para generar la respuesta

Los embeddings se persisten en disco (`embeddings_cache.json`) para no recalcularlos en cada ejecución.

## Stack

- `google-genai` — embeddings y generación
- `pypdf` — extracción de texto de PDFs
- `numpy` — similitud coseno
- `python-dotenv` — manejo de variables de entorno

## Requisitos

- Python 3.10+
- API key de Google Gemini (gratuita en [aistudio.google.com](https://aistudio.google.com))

## Instalación

```bash
git clone https://github.com/Ceskard26/mi-primer-rag.git
cd mi-primer-rag
python -m venv venv
source venv/Scripts/activate  # Windows
# source venv/bin/activate    # Mac/Linux
pip install -r requirements.txt
```

Crea un archivo `.env` en la raíz del proyecto:

```
GOOGLE_API_KEY=tu_api_key_aqui
```

Agrega tus PDFs a la carpeta `data/` y ejecuta:

```bash
python rag_ibm.py
```

En mi caso agregué 3 PDFs de IBM docs que contenían iformación sobre WatsonX, en tu caso puedes probar con PDF's de cualquier tema :)

## Ejemplo de uso

<img width="650" height="206" alt="image" src="https://github.com/user-attachments/assets/f32f97f6-78ac-45ca-866c-36b35b9487dc" />

## Notas

- El agente responde únicamente con información de los documentos en `data/`
- Si la respuesta no está en los documentos, lo indica explícitamente
- Al agregar o modificar PDFs, elimina `embeddings_cache.json` para regenerar los embeddings
```

Crea el archivo y súbelo:

```bash
git add README.md
git commit -m "add README"
git push origin main
```
