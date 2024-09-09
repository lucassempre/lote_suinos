FROM python:3.8.2-buster as backend

ARG DJANGO_ENV

ENV DJANGO_ENV=${DJANGO_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100


RUN apt update && apt install -y \
  curl \
  libffi-dev \
  openssl \
  musl-dev \
  tini \
  && rm -rf /var/lib/apt/lists/*


WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN ["pip", "install", "-r", "requirements.txt"]

COPY . /app
RUN ["chmod", "+x", "/app/entrypoint/entrypoint.sh"]
RUN ["python", "/app/manage.py", "collectstatic", "--noinput"]
ENTRYPOINT ["/app/entrypoint/entrypoint.sh"]


FROM nginx:1.17.6 as server
COPY --from=backend /static/ /static/
COPY entrypoint/nginx.conf /etc/nginx/nginx.conf
