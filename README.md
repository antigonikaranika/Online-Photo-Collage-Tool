# Online Photo Collage Tool

An online web app to create horizontal or vertical photo collages with customizable borders, inspired by a project idea from **DevProjects**. Built with Flask, Celery, Redis, and Docker. The project's prompt can be found at [https://www.codementor.io/projects/web/online-photo-collage-tool-atx32mwend].

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

### 2. Automatic Cleanup

- Celery Beat automatically removes old collage files from `static/collages` after 30 minutes and the files from `static/uploads` everytime the page is refreshed.

---

## Environment Variables

Set the `REDIS_URL` for Flask, Celery, and Beat:

```env
REDIS_URL=redis://redis:6379/0
```

Handled automatically by `docker-compose.yml`.

---

## Local Development (without Docker)

> In case you don't have Docker installed

### 1. Install Python dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Start Redis (Linux)

```bash
sudo apt update
sudo apt install redis-server
sudo systemctl enable redis-server
sudo systemctl start redis-server
# Test that it is working
redis-cli ping
# Should return: PONG
```
Create an .env file inside backend/app and type:

```bash
REDIS_URL=redis://localhost:6379/0
```

If you want to stop the redis server type:

```bash
sudo systemctl stop redis
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

| Method | Endpoint             | Description                                              |
|--------|----------------------|----------------------------------------------------------|
| POST   | `/create-task`       | Creates image processing task and returns a task id      |
| GET    | `/task-status/<id>`  | Returns either IN_PROGRESS or a collage id (task status) |
| GET    | `/get-collage/<id>`  | Returns generated collage image                          |

---

## Screenshot of the website

<img width="1545" height="756" alt="image" src="https://github.com/user-attachments/assets/3d15ec93-7c5d-4447-ae59-a03d9ca28ff6" />


---

## Authors

- Developed by Antigoni Karanika
- Powered by Flask, Celery, Redis, Docker

---
