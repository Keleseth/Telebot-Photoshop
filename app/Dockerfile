FROM python:3.12-slim
WORKDIR /srv
COPY requirements.txt .
RUN pip install -U pip && pip install -r requirements.txt
COPY . /srv/app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
