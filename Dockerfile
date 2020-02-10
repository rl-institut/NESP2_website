FROM python:3.6.10-alpine3.10
MAINTAINER Pierre-Francois Duc <pierre-francois.duc@rl-institut.de>

# ENV DEBIAN_FRONTEND noninteractive

# options for gunicorn
ENV GUNICORN_CMD_ARGS=--bind=0.0.0.0:5000 --workers=2

#RUN apt-get update
RUN apk update
RUN apk add --virtual build-deps gcc python3-dev musl-dev
#RUN apt-get install -y python python-pip python-virtualenv gunicorn
#RUN apt-get install -y python python-pip python-virtualenv gunicorn
#RUN apt-get install python-psycopg2
RUN apk add postgresql-dev

COPY app/requirements.txt /
RUN pip install -r /requirements.txt
RUN pip3 install gunicorn
# Setup flask application
RUN mkdir -p /deploy
RUN mkdir -p /deploy/app
COPY app /deploy/app
RUN apk del build-deps
# RUN python deploy/app/setup_maps.py TODO: need to fix the path
WORKDIR /deploy/app

EXPOSE 5000

# Start gunicorn
#CMD ["/usr/bin/gunicorn", "index:app"]
CMD ["gunicorn", "index:app"]

