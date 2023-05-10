FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN apt update && apt -qy install gcc libjpeg-dev libxslt-dev \
    libpq-dev libmariadb-dev libmariadb-dev-compat gettext cron openssh-client flake8 locales vim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["gunicorn","-b","0.0.0.0:8000","django_friends.wsgi:application"]
