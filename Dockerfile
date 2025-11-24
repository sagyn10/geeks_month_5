FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Установим системные зависимости для psycopg2 и сборки пакетов
RUN apt-get update \
     && apt-get install -y --no-install-recommends \
         build-essential \
         gcc \
         libpq-dev \
         netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Копируем зависимости и устанавливаем их
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip \
    && pip install -r /app/requirements.txt

# Копируем проект
COPY . /app/

# Папка для собранных static файлов
RUN mkdir -p /vol/static

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "shop_api.wsgi:application", "--bind", "0.0.0.0:8000"]
