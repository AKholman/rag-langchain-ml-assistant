# Use official HF image
FROM python:3.10

# Set working dir
WORKDIR /app

# Install dependencies first (layer cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create data dirs inside container
RUN mkdir -p /data/hf_home /data/chroma_db /data

# Copy application files
COPY backend.py .
COPY rag_core.py .

# Copy data folders into /data inside container
COPY data/ /data/
COPY chroma_db/ /data/chroma_db/

# Expose HF space port
EXPOSE 7860

# Run FastAPI server
CMD ["uvicorn", "backend:app", "--host", "0.0.0.0", "--port", "7860"]
