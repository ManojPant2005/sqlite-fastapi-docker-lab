# Use small Python image
FROM python:3.11-slim

# Set work folder inside container
WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all your files (api.py, mydata.db, etc) into container
COPY . .

# Tell Docker that API runs on 8000
EXPOSE 8000

# Important: 0.0.0.0 is must inside Docker, not 127.0.0.1
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
