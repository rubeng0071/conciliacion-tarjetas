# Dockerfile

# Imagen base
FROM python:3.11-slim

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Crear directorio de trabajo
WORKDIR /app

# Copiar requerimientos y código
COPY requirements.txt ./
COPY src ./src
COPY files ./files
COPY main.py ./

# Instalar dependencias
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Instalar cron
RUN apt-get update && apt-get install -y cron

# Copiar cronjob y configurar
COPY crontab.txt /etc/cron.d/fiserv-cron
RUN chmod 0644 /etc/cron.d/fiserv-cron && crontab /etc/cron.d/fiserv-cron

# Crear el log
RUN touch /var/log/cron.log

# Comando de entrada
CMD cron && tail -f /var/log/cron.log