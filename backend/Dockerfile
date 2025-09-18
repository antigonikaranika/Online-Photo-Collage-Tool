FROM python:3.10-slim

WORKDIR /app

# Copy backend app code and install dependencies
COPY backend/app /app
COPY backend/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
