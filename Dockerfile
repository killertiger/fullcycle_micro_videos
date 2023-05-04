FROM  python:3.10.2-slim

RUN apt update && apt install -y --no-install-recommends default-jre

RUN useradd -ms /bin/bash python

USER python

WORKDIR /home/python/app/src

ENV PYTHONPATH=${PYTHONPATH}/home/python/app
ENV JAVA_HOME=/usr/lib/jvw/java-11-openjdk-amd64

CMD [ "tail", "-f", "/dev/null" ]