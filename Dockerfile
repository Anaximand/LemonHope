FROM python:3.10-alpine

RUN apk add alpine-sdk

RUN mkdir -p /opt/lemon/
WORKDIR /opt/lemon/

COPY Pipfile ./
COPY Pipfile.lock ./

RUN pip install pipenv \
    && pipenv install --system --deploy

COPY . .

CMD ["python3", "lemonHope.py"]
