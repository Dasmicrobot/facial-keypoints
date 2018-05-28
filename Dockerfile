FROM python:3.6.5

RUN mkdir -p /usr/src/www

WORKDIR /usr/src/www

ADD . .

WORKDIR app

RUN pip install -r requirements.txt

EXPOSE 8080

ENTRYPOINT [ "/usr/local/bin/gunicorn", "-w", "4", "-b", ":8080", "app:app" ]