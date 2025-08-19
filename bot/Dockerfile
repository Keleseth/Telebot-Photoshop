FROM python:3.12-slim
WORKDIR /srv
COPY requirements.txt .
RUN pip install -U pip && pip install -r requirements.txt
COPY . /srv/bot
CMD ["python", "-m", "bot.main"]