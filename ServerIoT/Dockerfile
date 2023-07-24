FROM python:3.9.17-slim-bullseye

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

CMD ["python", "http_server.py"]