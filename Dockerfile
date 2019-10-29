FROM ubuntu:18.04
MAINTAINER Pierre-Francois Duc <pierre-francois.duc@rl-institut.de>

ENV DEBIAN_FRONTEND noninteractive

# options for gunicorn
ENV GUNICORN_CMD_ARGS="--bind=0.0.0.0:5000 --workers=2"

RUN apt-get update
RUN apt-get install -y python python-pip python-virtualenv gunicorn

# Setup flask application
RUN mkdir -p /deploy
RUN mkdir -p /deploy/app
COPY app /deploy/app
RUN pip install -r /deploy/app/requirements.txt
WORKDIR /deploy/app

EXPOSE 5000

# Start gunicorn
CMD ["/usr/bin/gunicorn", "index:app"]

