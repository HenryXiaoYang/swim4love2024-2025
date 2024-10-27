FROM python:3.9.20

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "run.py", "--host","0.0.0.0", "--port", "4000", "--environment", "production"]