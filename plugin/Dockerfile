FROM python:3.7

WORKDIR /app

COPY ./tmp/requirements.txt /app/
RUN pip install -r /app/requirements.txt
COPY ./tmp/vlad /app/vlad
COPY ./tmp/main.py /app/

ENTRYPOINT ["/usr/local/bin/python", "-u", "/app/main.py"]
