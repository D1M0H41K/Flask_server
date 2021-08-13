FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
ENV FLASK_APP todo:app

CMD [ "gunicorn", "-b", "0.0.0.0", "todo:app"]
