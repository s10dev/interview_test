FROM python:3.9-alpine


ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

RUN apk --update add
RUN apk add gcc libc-dev
RUN apk add postgresql-dev

RUN pip install --upgrade pip

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY ./survey_service/ .

ENTRYPOINT [ "/app/entrypoint.sh" ]