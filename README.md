# For local development, only database is running:
    docker-compose -f docker-db.local.yml up -d
    python -m venv venv
    uvicorn app.main:app --reload


# Production we run: 
    docker-compose -f docker-compose.prod.yml up -d --build
