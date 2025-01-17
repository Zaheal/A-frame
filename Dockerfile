FROM python:3.12.3-slim

RUN apt-get update && apt-get install python3-pip -y && pip install --upgrade pip && pip install pipenv

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers", "--workers", "5" ]