# backend.py
from fastapi import FastAPI
from pydantic import BaseModel
from app import answer_query  # import RAG function from core app.py

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

# -----------------------------
# Run locally with uvicorn
# -----------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend:app", host="0.0.0.0", port=8000, reload=True)
