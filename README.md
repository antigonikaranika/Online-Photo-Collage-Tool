# Online Photo Collage Tool

An online web app to create horizontal or vertical photo collages with customizable borders. Built with Flask, Celery, Redis, and Docker.

---

## Features

- Upload multiple images to create a collage
- Choose between horizontal or vertical layout
- Customize border size and color
- Collage preview and download
- Asynchronous task processing with Celery + Redis
- Auto-deletion of old collages (via scheduled cleanup)

---

## Folder Structure

```
online-photo-collage-tool/
├── backend/
│   ├── app/
│   │   ├── static/               # Uploaded and generated images
│   │   │   ├── uploads/
│   │   │   └── collages/
│   │   ├── utils/
│   │   │   └── image_processing.py
│   │   ├── app.py                # Flask app
│   │   ├── celery_config.py
│   │   ├── tasks.py
│   │   ├── worker.py
│   │   └── ...
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── script.js
├── docker-compose.yml
└── README.md
```

---

## Run with Docker

> Make sure you have **Docker** and **Docker Compose** installed.

### 1. Build & Start the Project

```bash
docker-compose up --build
```

- The Flask app will be available at: [http://localhost:5000](http://localhost:5000)
- Redis runs internally on port `6379`
- Collages are stored under `backend/app/static/collages`

### 2. Automatic Cleanup

- Celery Beat automatically removes old collage files from `static/collages` after 30 minutes and everytime the page is refreshed.

---

## Environment Variables

Set the `REDIS_URL` for Flask, Celery, and Beat:

```env
REDIS_URL=redis://redis:6379/0
```

Handled automatically by `docker-compose.yml`.

---

## 🧪 Local Development (without Docker)

> Optional — in case you don't have Docker installed

### 1. Install Python dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Start Redis (locally)

```bash
docker run -p 6379:6379 redis
```

### 3. Run Flask App

```bash
cd backend/app
python app.py
```

### 4. Start Celery Worker

```bash
celery -A celery_config worker --loglevel=info
```

### 5. Start Celery Beat (for cleanup tasks)

```bash
celery -A celery_config beat --loglevel=info
```

---

## API Endpoints

| Method | Endpoint             | Description                              |
|--------|----------------------|------------------------------------------|
| POST   | `/create-task`       | Submits images + settings for processing |
| GET    | `/task-status/<id>`  | Checks task status                       |
| GET    | `/get-collage/<id>`  | Returns generated collage image          |

---

## Screenshot

<img width="1545" height="756" alt="image" src="https://github.com/user-attachments/assets/3d15ec93-7c5d-4447-ae59-a03d9ca28ff6" />


---

## Authors

- Developed by Antigoni Karanika
- Powered by Flask, Celery, Redis, Docker

---
