#Base Image
FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py migrate

EXPOSE 9002


# CMD python manage.py runserver 0.0.0.0:8003
CMD gunicorn hrgpt.wsgi:application --bind 0.0.0.0:9002