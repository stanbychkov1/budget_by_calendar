FROM python:3.8.6-slim-buster

WORKDIR /code

COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

COPY . .
ENTRYPOINT ["/docker-entrypoint.sh"]