FROM python:3.6.5-slim

ADD app app/
ADD detector_architectures detector_architectures/

WORKDIR app

RUN pip install -r requirements.txt

EXPOSE 8080

CMD [ "gunicorn -w 4 -b 127.0.0.1:8080 app:app" ]