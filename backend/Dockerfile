# Use a Python base image (ensure it's compatible with 'torch')
FROM python:3.11-slim

# Set environment variable for Hugging Face model cache (good practice for Spaces)
ENV HF_HOME /data/hf_home

# Set working directory
WORKDIR /app

# Copy requirements and install them first for layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Create directories for data and model cache. Note: /data is writable on HF Spaces.
RUN mkdir -p /data/hf_home /app/data /app/chromodb 

# !!! CRITICAL CHANGE: Run the scraper to populate the initial data !!!
# This runs once during the build process.
RUN python scraper.py

# Expose the port that the FastAPI app will run on
EXPOSE 8000

# Command to run the FastAPI application using uvicorn/gunicorn
# The backend.py file uses os.environ.get("PORT", 7860) but we will use the default uvicorn behavior 
# which is simpler when EXPOSE is set.
# Using 'gunicorn' with 'uvicorn.workers.UvicornWorker' is a better production practice than raw uvicorn.run()
# This command starts the backend.py application on 0.0.0.0:8000
CMD ["gunicorn", "backend:app", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]