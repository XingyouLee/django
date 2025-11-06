FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt


COPY . /app/
RUN python manage.py collectstatic --noinput

# ✅ Cloud Run 会注入 PORT 环境变量（默认 8080）
ENV PORT=8080

# ✅ 使用 Gunicorn（生产环境）
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 60 my_site.wsgi:application