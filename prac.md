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


# Why Docker
# What is Docker doing in YOUR project?
Right now you have this without Docker:

Your Windows -> Python installed -> `python -m uvicorn api:app --reload` -> API runs

If your friend wants to run it, he must install Python, pip install fastapi, etc.

# With Docker, you have this:


Your Windows -> Docker Desktop -> Container (inside it has Python + your api.py + mydata.db) -> API runs on http://localhost:8000


# Why we use it in your project?

Your mydata.db is a file. In Docker with volume, it never gets lost.
You can give your whole folder to anyone, they just do docker-compose up and it works - no Python install needed.
Same environment everywhere - your Windows, my laptop, production server.


# What happens when you do docker-compose up --build ?
This is what happened in your logs:

Building -> Reads your Dockerfile, makes an IMAGE called sqllite-api (Python + fastapi + your code copied)
Creating Network + Creating Container -> Makes a CONTAINER called sqlite_api from that image
Attaching to sqlite_api -> Inside container it runs: uvicorn api:app --host 0.0.0.0 --port 8000
Volumes: ./mydata.db:/app/mydata.db -> Your Windows file and container file become SAME file. So if API adds a user, your local mydata.db also updates.
All your things running means: The container is running and uvicorn is running inside it.

# How to manage it - your daily commands
Open PowerShell in D:\Manoj\Learn\SqlLite\

1. Start (what you did):
Open PowerShell in D:\Manoj\Learn\SqlLite\

docker-compose up --build

This builds + starts. You see logs live. If you press CTRL+C, it stops.

2. Start in background (so you can close terminal):
docker-compose up -d --build

3. Check if running
docker-compose ps
docker ps

You should see sqlite_api Up.

4. See logs:
docker-compose logs -f
-f = follow logs live.

5. Stop (pause, data stays safe):
docker-compose stop
Container stops, but NOT deleted. Your mydata.db is safe because of volume. To start again:

docker-compose start



6. Restart (when you change api.py):

docker-compose restart


Because we have volume ./api.py:/app/api.py, your code auto-reloads anyway, you don't even need restart most times.

7. Full shutdown (delete container, keep image):
docker-compose down

This stops and DELETES the container, but image stays. Your mydata.db is STILL safe on Windows because of volume. Next time you do up, it creates fresh container.

IMPORTANT: Never do docker-compose down -v - the -v would delete volumes and you would lose your SQLite data if you didn't have file volume.

Is it auto shut down or what?
No, not auto.

If you did docker-compose up (without -d): It shuts down when you press CTRL+C or close terminal.
If you did docker-compose up -d: It keeps running in background, even if you close VS Code. It only stops when you do docker-compose stop or down, or you restart your PC.
We have restart: unless-stopped in compose file, so if your PC restarts, Docker will auto-start your API again.
You can also manage from Docker Desktop app:
Open Docker Desktop -> Left side Containers -> You will see sqlite_api -> There you have buttons: Stop, Start, Restart, Delete - same as commands.


# For your learning, use this workflow daily:


# Morning start work
docker-compose up -d
# See API
# http://localhost:8000/docs
# Evening stop work
docker-compose stop
