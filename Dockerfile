FROM python:3.6.10-alpine3.10
MAINTAINER Pierre-Francois Duc <pierre-francois.duc@rl-institut.de>

ARG branch=dev

# options for gunicorn
ENV GUNICORN_CMD_ARGS=--bind=0.0.0.0:5000 --workers=2

RUN apk update
RUN apk add --virtual build-deps gcc musl-dev postgresql-dev git

# this helps using the cache of docker
COPY app/requirements.txt /
RUN pip install -r /requirements.txt
RUN pip3 install gunicorn
RUN git clone --single-branch --branch $branch https://github.com/rl-institut/NESP2.git

# Setup flask application
RUN mkdir -p /src
COPY app /app

RUN python /app/setup_maps.py -docker

WORKDIR /app

EXPOSE 5000

# Start gunicorn
CMD ["gunicorn", "index:app"]

