FROM python:3.12.4-slim


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH '/opt/app'

WORKDIR /opt/app
COPY requirements.txt /opt/app/requirements.txt
RUN apt-get update && apt-get install -y git curl
RUN  pip install --upgrade pip\
     && pip install --no-cache-dir -r /opt/app/requirements.txt

COPY . /opt/app

CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8000"]
