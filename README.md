# Telebot Photoshop

Коммерческий проект: Telegram‑бот для обработки фотографий с использованием FastAPI и Docker‑инфраструктуры.

---

### Технологии и инструменты
![Python](https://img.shields.io/badge/python-3.12-blue?style=for-the-badge&logo=python&logoColor=white)
![Aiogram](https://img.shields.io/badge/aiogram-3.x-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)
![FastAPI](https://img.shields.io/badge/fastapi-0.116-green?style=for-the-badge&logo=fastapi)
![Redis](https://img.shields.io/badge/redis-7-red?style=for-the-badge&logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![GitHubActions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)

---

## Описание проекта

Проект разработан для автоматизации обработки изображений и взаимодействия с пользователями через Telegram-бота.
Цель — предоставить пользователям простой инструмент для загрузки и редактирования фотографий (например, удаление или замена фона, выбор цвета, настройка параметров), а администраторам — базовые средства управления доступом и ограничениями.

В архитектуре используется отдельный backend на FastAPI, отвечающий только за обработку запросов от бота через API, работающего по внутреннему адресу сервера. Все сервисы изолированы и управляются через Docker-инфраструктуру.

Основной функционал:
- Загрузка и обработка изображений пользователями в чат с ботом.
- Удаление или замена фона с возможностью выбора цвета через WebApp.
- Ограничение числа запросов на обработку фотографий (лимиты на пользователя).
- Поддержка whitelist/blacklist пользователей через Redis.
- Кнопка Отмена для удобного выхода из сценария обработки.
- CI/CD через GitHub Actions: автоматическая сборка и публикация образов в Docker Hub, деплой на сервер.
- Асинхронная работа сервисов на базе FastAPI, Aiogram и Redis.

---

## Начало работы

### Деплой на сервер (CI/CD)

Деплой настроен через **GitHub Actions**. При пуше в ветки `main` и `develop`:
1) собираются Docker-образы `telebot-bot` и `telebot-api`;
2) образы пушатся в Docker Hub (`:SHA`, а для `main` дополнительно `:latest`);
3) по SSH выполняется деплой на сервер: `docker compose pull && docker compose up -d`.

#### Секреты репозитория (Settings → Secrets → Actions)
- `DOCKERHUB_USERNAME` — логин Docker Hub  
- `DOCKERHUB_TOKEN` — токен/пароль Docker Hub  
- `SERVER_HOST` — IP/домен сервера  
- `SERVER_USER` — SSH-пользователь (например, `ubuntu`)  
- `SERVER_SSH_KEY` — приватный SSH-ключ (`-----BEGIN OPENSSH PRIVATE KEY----- ...`)
- `SERVER_PROJECT_DIR` - название директория на продакшен сервере, куда будет произведен деплой ci/cd например *telebot_photoshop*

> `GITHUB_TOKEN` выдаётся автоматически, добавлять не нужно.

### Требования на сервере (один раз)
- Установлены **Docker** и **Docker Compose**.
- Создан каталог проекта (например, *telebot_photoshop*) по пути `${SERVER_USER}/<значение SERVER_PROJECT_DIR из Secrets>`.
- В каталоге проекта размещён файл `docker-compose.yml` (прод-версия).
- В каталоге проекта создан файл `.env` на основе примера `.env.example`.

---

## 🛠️ Локальный запуск

- Клонировать репозиторий и перейти в директорию проекта:
```bash
git clone <URL_РЕПОЗИТОРИЯ>
cd telebot_photoshop
```
- Создать файл .env на основе примера .env.example и заполнить переменные окружения.
- Собрать и запустить контейнеры с использованием локального конфига:
```bash
docker compose -f docker-compose.local.yml up --build
```
После запуска бот будет доступен в Telegram
