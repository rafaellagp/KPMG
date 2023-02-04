FROM python:3.10

RUN mkdir /app
WORKDIR /app

COPY classification /app

RUN pip3 install -r requirements.txt

CMD [ "python", "main.py" ]