Commands
In VS Code terminal, in your SqlLite folder:
# 1. Build - creates image with Python + FastAPI + your code
docker build -t sqlite-api .

# 2. Run - starts container
docker run -p 8000:8000 -v ${PWD}/mydata.db:/app/mydata.db sqlite-api

ren Requirements.txt requirements.txt
ren Docker-Compose.yml docker-compose.yml


docker build -t sqlite-api .

docker-compose up --build


# The problem I fixed:

Before: Requirements.txt capital R -> Docker (Linux) couldn't find it
After: requirements.txt small r -> build success FINISHED 10/10

# 2. What actually happened:
Our files (api.py + mydata.db)
      |
      -> Dockerfile = Recipe (FROM python:3.11-slim, COPY, RUN pip install)
      |
      -> docker build = Makes IMAGE (sqllite-api) - like a snapshot
      |
      -> docker-compose up = Makes CONTAINER (sqlite_api) from image + runs it
      |
      -> http://localhost:8000/users = our API now running inside container, not directly on Windows