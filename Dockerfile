FROM python:3.6-alpine

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

COPY app app
COPY migrations migrations
COPY neuroflow.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP neuroflow.py

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]