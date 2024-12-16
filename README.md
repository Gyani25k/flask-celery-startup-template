# Flask-Celery Startup Template

A **Flask** and **Celery** integrated project template designed for building scalable, asynchronous web applications. This template serves as a quick starting point for developers to create backend projects with background task support using **Celery**.

---

## Features
- **Flask**: A lightweight web framework for building APIs and web apps.
- **Celery**: Supports background task execution and scheduling.
- **Dockerized Setup**: Includes `Dockerfile` and `docker-compose.yml` for easy development and deployment.
- **Modular Structure**: Organized project structure for scalability and clarity.
- **Redis** as Message Broker: Default Celery message broker for task queue management.

---

## Project Structure

```plaintext
flask-celery-startup-template/
│
├── app/                      # Application code
│   ├── __init__.py           # Initializes Flask app and Celery instance
│   ├── routes.py             # API routes and views
│   ├── tasks.py              # Background tasks handled by Celery
│   ├── models.py             # Database models (if needed)
│
├── instance/                 # Instance-specific files (configurations, etc.)
│
├── docker-compose.yml        # Docker Compose setup for Flask, Celery, and Redis
├── Dockerfile                # Dockerfile to build Flask-Celery app
├── requirements.txt          # Dependencies
└── README.md                 # Project documentation
```

---

## Installation and Setup

### 1. **Clone the Repository**
```bash
git clone https://github.com/Gyani25k/flask-celery-startup-template.git
cd flask-celery-startup-template
```

### 2. **Setup Environment**
Ensure you have Python and Docker installed. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. **Run Using Docker**
Start the Flask server, Celery worker, and Redis message broker:
```bash
docker-compose up --build
```
- Flask will run on `http://localhost:5000`
- Celery worker will connect to Redis.

### 4. **Run Without Docker** (Optional)
If you prefer not to use Docker:
1. Start Redis server (ensure it’s running on `localhost:6379`).
2. Run the Flask application:
   ```bash
   flask run
   ```
3. Start the Celery worker:
   ```bash
   celery -A app.tasks.celery worker --loglevel=info
   ```

---

## Example Usage

### **Defining a Background Task** (tasks.py)
```python
from celery import Celery
from flask import current_app

celery = Celery('tasks', broker='redis://localhost:6379/0')

@celery.task
def add(x, y):
    return x + y
```

### **Trigger Task from Route** (routes.py)
```python
from flask import Flask, jsonify
from app.tasks import add

app = Flask(__name__)

@app.route("/add/<int:x>/<int:y>", methods=["GET"])
def start_task(x, y):
    result = add.delay(x, y)
    return jsonify({"task_id": result.id, "status": "Task started"})
```

### **Check Task Result**
- Use Celery's result backend to fetch task results:
```python
from celery.result import AsyncResult

@app.route("/result/<task_id>", methods=["GET"])
def get_result(task_id):
    result = AsyncResult(task_id)
    return jsonify({"task_status": result.status, "task_result": result.result})
```

---

## Contributing
Contributions are welcome! Please open an issue or submit a pull request if you want to improve this template.

---

## License
This project is licensed under the MIT License.

---

## Contact
For questions, issues, or suggestions, please reach out:
- **GitHub**: [Your GitHub Profile](https://github.com/Gyani25k)

---

**Happy Coding! 🚀**
