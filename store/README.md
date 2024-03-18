# Store

## Locally

1. Install the project dependencies:
```bash
pip install -r requirements.txt
```
2. Run the system:
```bash
uvicorn main:app --host 0.0.0.0
```

## Docker

1. Open docker folder
```bash
cd docker
```
2. Build and Up containers
```bash
docker-compose up -d --build
```