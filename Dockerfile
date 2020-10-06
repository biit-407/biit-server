FROM python:3.7

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . .

RUN pip install -r requirements.txt
RUN pip install gunicorn

CMD exec source envfile
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 main:app