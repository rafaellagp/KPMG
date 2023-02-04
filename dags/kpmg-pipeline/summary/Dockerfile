FROM python:3.10

RUN mkdir /app
WORKDIR /app

COPY summary /app

RUN pip3 install -r requirements.txt

CMD [ "python", "main.py" ]