FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Flask app code
COPY backend/app/ .

# Copy frontend files (served by Flask)
COPY frontend/ ./frontend/

# Expose Flask default port
EXPOSE 5000

# Default command to run Flask app
CMD ["python", "app.py"]
