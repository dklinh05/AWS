FROM python:3.11-slim

WORKDIR /app

# Copy requirements file first to leverage Docker cache
COPY requirements.txt .

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend logic and frontend templates
COPY src/ ./src/
COPY frontend/ ./frontend/

# Expose the API port
EXPOSE 8000

# Run the FastAPI app with uvicorn
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
