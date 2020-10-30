FROM python:3.7.6-buster
MAINTAINER Pierre-Francois Duc <pierre-francois.duc@rl-institut.de>

ARG branch=master
ARG POSTGRES_url
ARG POSTGRES_user
ARG POSTGRES_pw
ARG POSTGRES_db

ENV POSTGRES_URL=$POSTGRES_url
ENV POSTGRES_USER=$POSTGRES_user
ENV POSTGRES_PW=$POSTGRES_pw
ENV POSTGRES_DB=$POSTGRES_db

COPY docker_postgres_login_help.py /
COPY app /app
COPY index.py /

#make python and pip working for numpy
#ADD repositories /etc/apk/repositories
RUN apt update
RUN apt-get -y  install git  

# options for gunicorn
ENV GUNICORN_CMD_ARGS=--bind=0.0.0.0:8000 --workers=2


# this helps using the cache of docker
RUN /usr/local/bin/python -m pip install --upgrade pip
COPY app/requirements.txt /
RUN pip install -r /requirements.txt
RUN pip install gunicorn
RUN git clone --single-branch --branch $branch https://github.com/rl-institut/NESP2.git

# Setup flask application
RUN mkdir -p /src


#RUN python /app/setup_maps.py -docker

#WORKDIR /app

#EXPOSE 5000 

RUN python /docker_postgres_login_help.py


# Start gunicorn
#RUN gunicorn index:app -b 127.0.0.1:8000 -D

#CMD ["gunicorn", "index:app"]
