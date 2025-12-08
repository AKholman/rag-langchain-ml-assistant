# -----------------------------
# Base image
# -----------------------------
FROM python:3.10

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# -----------------------------
# Install system dependencies
# -----------------------------
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# -----------------------------
# Set working directory
# -----------------------------
WORKDIR /app

# -----------------------------
# Copy requirements
# -----------------------------
COPY requirements.txt .

# -----------------------------
# Install Python packages
# -----------------------------
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# -----------------------------
# Copy all project files
# -----------------------------
COPY . .

# -----------------------------
# Expose FastAPI port
# -----------------------------
EXPOSE 8000

# -----------------------------
# Start backend API
# -----------------------------
CMD ["uvicorn", "backend:app", "--host", "0.0.0.0", "--port", "8000"]
