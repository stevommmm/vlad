FROM python:3.7

WORKDIR /app

COPY ./requirements.txt /app/
RUN pip install -r /app/requirements.txt
COPY ./vlad /app/vlad
COPY ./main.py /app/

ENTRYPOINT ["/usr/local/bin/python", "-u", "/app/main.py"]
