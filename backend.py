# backend.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag_core import answer_query

app = FastAPI(title="ML RAG Backend (HF)")

# CORS (required for calling from Gradio Space)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class Query(BaseModel):
    question: str

@app.post("/ask")
def ask(query: Query):
    try:
        res = answer_query(query.question)
        return res
    except Exception as e:
        return {"error": str(e)}


# HF uses uvicorn to start the server
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)


