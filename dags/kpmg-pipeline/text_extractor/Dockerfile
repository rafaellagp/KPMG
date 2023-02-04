FROM python:3.10

RUN mkdir /app
WORKDIR /app

COPY text_extractor /app
COPY utils/download_file.py /app/utils/download_file.py

RUN apt update -y
RUN apt upgrade -y
RUN apt install libgl1 -y

RUN pip3 install -r requirements.txt

CMD [ "python", "main.py" ]