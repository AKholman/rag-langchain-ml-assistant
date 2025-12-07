# rag_core.py (core RAG logic - LOCAL TRANSFORMERS VERSION)
import json
from pathlib import Path
import os

# IMPORTANT FOR RENDER: store HF models in /tmp (ephemeral disk)
os.environ["HF_HOME"] = "/tmp"

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Local transformers LLM
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# -----------------------------
# CONFIG
# -----------------------------
DATA_FILE = Path("data/wikidata_ml.json")
PERSIST_DIR = "chroma_db"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

LLM_MODEL = "google/flan-t5-large"   # local LLM model

# -----------------------------
# Load local LLM once at startup
# -----------------------------
print("Loading local FLAN-T5 model...")
tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL)
model = AutoModelForSeq2SeqLM.from_pretrained(LLM_MODEL)

llm_pipeline = pipeline(
    "text2text-generation",
    model=model,
    tokenizer=tokenizer,
    device=-1,            # CPU. Change to device=0 for GPU
)

# -----------------------------
# 1. Load documents
# -----------------------------
def load_documents():
    docs = []
    if not DATA_FILE.exists():
        return docs
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        items = json.load(f)
    for it in items:
        text = f"{it.get('title','')}\n\n{it.get('description','')}\n\n{it.get('url','')}"
        docs.append(Document(page_content=text, metadata={"id": it.get("id"), "title": it.get("title")}))
    return docs

# -----------------------------
# 2. Vector store
# -----------------------------
def get_or_create_vectorstore(force_recreate=False):
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    if force_recreate or not Path(PERSIST_DIR).exists() or not any(Path(PERSIST_DIR).iterdir()):
        print("Creating new vector store...")
        docs = load_documents()
        if not docs:
            raise ValueError("No documents found. Run scraper first.")

        splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=200)
        split_docs = splitter.split_documents(docs)

        vectordb = Chroma.from_documents(split_docs, embeddings, persist_directory=PERSIST_DIR)

    else:
        print("Loading existing vector store...")
        vectordb = Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)

    return vectordb

# -----------------------------
# 3. RAG
# -----------------------------
PROMPT = """Use the following context to answer the user's question as an ML support assistant.
Context:
{context}
Question: {question}
Answer concisely and include sources if possible.
"""

def answer_query(query: str, top_k: int = 4):
    # 1. Retrieve
    vectordb = get_or_create_vectorstore()
    retriever = vectordb.as_retriever(search_kwargs={"k": top_k})
    docs = retriever.invoke(query)

    context = "\n\n".join([
        f"{d.page_content}\n[source: {d.metadata.get('title','')}]"
        for d in docs
    ])

    # 2. Build prompt
    prompt = PromptTemplate(input_variables=["context", "question"], template=PROMPT)
    formatted_prompt = prompt.format(context=context, question=query)

    # 3. Run local LLM
    try:
        out = llm_pipeline(
            formatted_prompt,
            max_new_tokens=512,
            do_sample=False
        )[0]["generated_text"]
    except Exception as e:
        print("\n--- RAG LOCAL LLM ERROR ---")
        print(e)
        print("--- END ERROR ---\n")
        raise Exception(f"Local LLM error: {e}")

    if not out:
        out = "Model returned an empty response."

    return {
        "answer": out,
        "retrieved": [{"title": d.metadata.get("title"), "text": d.page_content[:500]} for d in docs]
    }
