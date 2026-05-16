# Use the official Python 3.12 slim image to keep the container small
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Install OS dependencies required by OpenCV
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Expose port 8000
EXPOSE 8000

# Start the FastAPI server using Uvicorn
CMD ["uvicorn", "translation-back.main_api:app", "--host", "0.0.0.0", "--port", "8000"]
