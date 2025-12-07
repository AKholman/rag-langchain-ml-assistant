# backend.py
from fastapi import FastAPI
from pydantic import BaseModel
from rag_core import answer_query  # import RAG function from core app.py

app = FastAPI(title="ML RAG Backend")

# -----------------------------
# Request model
# -----------------------------
class Query(BaseModel):
    question: str

# -----------------------------
# Endpoint to ask a question
# -----------------------------
@app.post("/ask")
def ask(query: Query):
    try:
        res = answer_query(query.question)
        return res
    except Exception as e:
        return {"error": str(e)}


