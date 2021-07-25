FROM python:3.8-slim-buster

WORKDIR /continental_docker_python_service_solution

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP=app.py
CMD flask run --host=0.0.0.0 --port=${PORT}