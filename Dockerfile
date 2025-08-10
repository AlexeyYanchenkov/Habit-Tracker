FROM python:3.10.12

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential gcc libffi-dev libssl-dev python3-dev cargo pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Обновляем pip и инструменты сборки, и ставим Cython заранее
RUN pip install --upgrade pip setuptools wheel
RUN pip install cython

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN python manage.py collectstatic --noinput || true

CMD ["gunicorn", "habits_project.wsgi:application", "--bind", "0.0.0.0:8000"]
