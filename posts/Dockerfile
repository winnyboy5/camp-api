FROM python:3.8

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 5003

ENTRYPOINT ["./gunicorn.sh"]