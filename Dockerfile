FROM python:3.7
MAINTAINER desertkun
RUN apt-get update && apt-get install -y python3-dev libssl-dev libffi-dev musl-dev make gcc g++ libzmq5 libzmq3-dev curl libtool autoconf automake
WORKDIR /tmp
COPY anthill /tmp/anthill
COPY setup.py /tmp
RUN pip install .
RUN rm -rf /tmp
