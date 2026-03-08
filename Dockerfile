FROM python:3.14-alpine3.23
ARG VERSION

RUN apk add alpine-sdk

RUN mkdir -p /opt/lemon/
WORKDIR /opt/lemon/

COPY Pipfile ./
COPY Pipfile.lock ./

RUN pip install pipenv \
  && pipenv install --system --deploy

COPY . .

RUN echo $VERSION > VERSION_FILE

CMD ["python3", "lemonHope.py"]
