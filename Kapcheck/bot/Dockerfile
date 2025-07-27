FROM python:3.10

RUN apt-get update
RUN pip install --upgrade pip

WORKDIR /app

COPY . /app/

RUN pip install -r requirements.txt

CMD ["python", "bot.py"]
