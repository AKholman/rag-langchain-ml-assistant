# app.py (frontend)
import gradio as gr
import requests

# Backend URL
BACKEND_URL = "https://rag-langchain-ml-assistant.onrender.com/query"

def respond(query):
    try:
        response = requests.post(BACKEND_URL, json={"question": query})
        response.raise_for_status()
        data = response.json()

        # Ensure "answer" exists
        if "answer" in data:
            return data["answer"]
        elif "error" in data:
            return f"Backend error: {data['error']}"
        else:
            return "Unexpected backend response."

    except requests.exceptions.RequestException as e:
        return f"Error connecting to backend: {e}"

# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("# ML RAG Assistant (via FastAPI Backend)")
    inp = gr.Textbox(label="Question", placeholder="Ask about transformers, embeddings, PyTorch...")
    btn = gr.Button("Ask")
    out = gr.Textbox(label="Answer")
    btn.click(fn=respond, inputs=inp, outputs=out)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
