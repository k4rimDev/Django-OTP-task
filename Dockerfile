FROM python:3.11-slim

ARG DIR=/app

WORKDIR $DIR

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && apt-get clean

COPY requirements.txt ./

RUN python3 -m pip install --upgrade pip

RUN python3 -m pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]
