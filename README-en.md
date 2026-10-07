# Telebot Photoshop

Commercial project: a Telegram bot for photo editing, built on FastAPI and a Docker-based infrastructure.

---

### Technologies and tools
![Python](https://img.shields.io/badge/python-3.12-blue?style=for-the-badge&logo=python&logoColor=white)
![Aiogram](https://img.shields.io/badge/aiogram-3.x-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)
![FastAPI](https://img.shields.io/badge/fastapi-0.116-green?style=for-the-badge&logo=fastapi)
![Redis](https://img.shields.io/badge/redis-7-red?style=for-the-badge&logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![GitHubActions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)

---

## Project description

The project was built to automate image processing and user interaction through a Telegram bot.
The goal is to give users a simple way to upload and edit photos (e.g. removing or replacing the background, picking a color, adjusting parameters), and to give admins basic tools for access control and limits.

The architecture uses a separate FastAPI backend, responsible only for processing requests from the bot through an API reachable at the server's internal address. All services are isolated and managed through the Docker infrastructure.

Core functionality:
- Users upload and process images directly in the chat with the bot.
- Background removal or replacement, with color selection through a WebApp.
- Daily per-user limit on photo-processing requests.
- Whitelist/blacklist support via Redis.
- A Cancel button for easily backing out of the processing flow.
- CI/CD via GitHub Actions: automatic image builds, publishing to Docker Hub, and deployment to the server.
- Asynchronous services built on FastAPI, Aiogram, and Redis.

---

## Getting started

### Deploying to a server (CI/CD)

Deployment is configured through **GitHub Actions**. On a push to the `main` or `develop` branches:
1) the `telebot-bot` and `telebot-api` Docker images are built;
2) the images are pushed to Docker Hub (`:SHA`, and additionally `:latest` for `main`);
3) deployment to the server runs over SSH: `docker compose pull && docker compose up -d`.

#### Repository secrets (Settings → Secrets → Actions)
- `DOCKERHUB_USERNAME` - Docker Hub username
- `DOCKERHUB_TOKEN` - Docker Hub token/password
- `SERVER_HOST` - server IP/domain
- `SERVER_USER` - SSH user (e.g. `ubuntu`)
- `SERVER_SSH_KEY` - private SSH key (`-----BEGIN OPENSSH PRIVATE KEY----- ...`)
- `SERVER_PROJECT_DIR` - name of the directory on the production server the CI/CD deploy targets, e.g. *telebot_photoshop*

> `GITHUB_TOKEN` is provided automatically, no need to add it.

### Server requirements (one-time setup)
- **Docker** and **Docker Compose** installed.
- A project directory created (e.g. *telebot_photoshop*) at `${SERVER_USER}/<value of SERVER_PROJECT_DIR from Secrets>`.
- A `docker-compose.yml` (production version) placed in the project directory.
- A `.env` file created in the project directory, based on the `.env.example` sample.

---

## 🛠️ Local setup

- Clone the repository and go into the project directory:
```bash
git clone <REPOSITORY_URL>
cd telebot_photoshop
```
- Create a `.env` file based on the `.env.example` sample and fill in the environment variables.
- Build and start the containers using the local config:
```bash
docker compose -f docker-compose.local.yml up --build
```
Once started, the bot will be available on Telegram.

---

## Additional information
API docs are available once the server is running at:
- `http://localhost:8000/docs` - Swagger UI
- `http://localhost:8000/redoc` - Redoc UI
