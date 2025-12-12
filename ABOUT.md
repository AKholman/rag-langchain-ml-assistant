
🤖 ML RAG Assistant: Decoupled FastAPI and Gradio Deployment

This project implements a complete Retrieval-Augmented Generation (RAG) system featuring a fully decoupled, production-ready architecture. It is deployed across two separate Hugging Face Spaces: a Dockerized FastAPI backend and a Gradio frontend.

The core system utilizes local, open-source models for all heavy computation, ensuring full control over the RAG pipeline without relying on external, paid API services (like OpenAI).


✨ Key Features & Components

1. 🌐 Decoupled Deployment (CI/CD)
The application is split into two distinct services, enabling scalable, independent updates and maintenance:

    A) Backend Space (Docker/FastAPI): Hosts the heavy RAG logic, LLM, and vector store.
        1) Technology: Docker container running a FastAPI web service.

    B) Frontend Space (Gradio): Provides the interactive chat interface.
        1)Technology: Gradio SDK app that sends queries to the remote FastAPI backend API.

    C) Automation: Continuous Integration/Continuous Deployment (CI/CD) via GitHub Actions ensures changes 
       to the backend/ or frontend/ directories automatically update the correct Space.


2. 🧠 Retrieval-Augmented Generation (RAG) Pipeline
The RAG engine is built using LangChain and runs 100% locally within the backend container.
________________________________________________________________________________________________________
|      Component     |         Technology        |                    Description                       |
|--------------------|---------------------------|------------------------------------------------------|
|  Knowledge Base    | data/wikidata_ml.json     | Scraped data on Machine Learning entities from       |
|                    |                           | Wikidata using a custom SPARQL scraper               |
|--------------------|---------------------------|------------------------------------------------------|
|  Embeddings        | sentence-transformers/all | Local, high-performance embeddings for transforming  |
|                    | -MiniLM-L6-v2             | text into vectors                                    |
|--------------------|---------------------------|------------------------------------------------------|
| Vector Store       |  ChromaDB                 | The vector database used for persistence (chroma_db/)| 
|                    |                           | and efficient similarity search (retrieval)          |
|--------------------|---------------------------|------------------------------------------------------|
| Large Language     |  FLAN-T5-Large            | A local, T5-based model from Hugging Face            |
| Model              |                           |  Transformers, used to generate the final,           | 
|                    |                           |  grounded answer                                     |
|____________________|___________________________|______________________________________________________|


3. 📦 Project Structure (Deployment View)The primary repository is structured to support the decoupled CI/CD setup:

project/
├── .github/
│   ├── deploy_backend.yml   # CI/CD for Docker Space
│   └── deploy_frontend.yml  # CI/CD for Gradio Space
├── backend/                 # Deployed to Docker Space (rag-api-backend)
│   ├── backend.py           # FastAPI entry point
│   ├── rag_core.py          # Core RAG logic
│   ├── scraper.py           # Wikidata scraper
│   ├── data/
│   └── chromadb/
└── frontend/                # Deployed to Gradio Space (rag-gradio-frontend)
    ├── app.py               # Gradio UI code
    └── frontend_requirements.txt



🚀 How It Works (Live Pipeline): 

1. User Input: The user asks a question in the Gradio UI.
2. API Call: frontend/app.py sends the question as a POST request to the remote FastAPI backend endpoint. 
3. Retrieval: The FastAPI server calls rag_core.py, which uses MiniLM embeddings to search the local ChromaDB for the most relevant documents from the Wikidata knowledge base.
4. Augmentation & Generation: The retrieved context and the user's question are combined into a final prompt and sent to the local FLAN-T5-Large LLM.
5. Response: The LLM's final answer, along with the source documents, is returned through FastAPI back to the Gradio UI.

