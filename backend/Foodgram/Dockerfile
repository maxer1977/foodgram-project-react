FROM python:3.9

WORKDIR /app

RUN pip install gunicorn==20.1.0

COPY . .

RUN pip install -r requirements.txt --no-cache-dir

CMD ["gunicorn", "Foodgram.wsgi:application", "--bind", "0.0.0.0:9000"]

ONBUILD RUN python manage.py makemigrations
ONBUILD RUN python manage.py migrate
ONBUILD RUN python manage.py collectstatic