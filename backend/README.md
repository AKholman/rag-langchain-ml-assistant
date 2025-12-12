---
title: ML RAG API Backend
emoji: 🐳
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 8000 # Critical: Specify the port the FastAPI app exposes
pinned: false
---

# ML RAG API Backend (Docker)

This Hugging Face Space hosts the FastAPI backend for the ML RAG Assistant. It includes the heavy LLM model, the Chroma vector store, and the core RAG logic.

The API is exposed at `https://alex-khol-rag-api-backend.hf.space/ask`.