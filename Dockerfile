FROM python:latest

WORKDIR /app

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY ./app .

CMD ["fastapi", "run", "--host", "0.0.0.0", "--port", "80"]