# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
# COPY requirements.txt .

# Install ffmpeg
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install dependencies
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install spleeter --no-deps
RUN pip install fastapi fastapi-cli --no-deps
RUN pip install pydub librosa uvicorn==0.30.1 numpy==1.26.4 pandas tensorflow

# Copy the rest of the application code
COPY . .

# Expose the port FastAPI will run on
EXPOSE 8000

# Run the FastAPI application using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
