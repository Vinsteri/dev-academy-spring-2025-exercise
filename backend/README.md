# Backend

I chose to use FastAPI for the backend. It is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.

## To run the backend

1. create venv
```bash
python -m venv dev-academy
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Make sure db container is running
```bash
docker compose up --build --renew-anon-volumes -d
```

4. Run backend
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

5. to run API test once backend is running
```bash
pytest
```
