FROM python:3.6-alpine

COPY . /app
RUN pip install -r /app/requirements.txt
RUN chmod 755 /app/slacks/slacks.py

WORKDIR /app

ENTRYPOINT ["/bin/sh", "-c", "/app/slacks/slacks.py \"$@\"", "--"]