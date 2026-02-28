FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create artifacts directory
RUN mkdir -p artifacts

# Copy model into expected path
COPY model.pkl artifacts/model.pkl

# Copy FastAPI app
COPY app.py .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
