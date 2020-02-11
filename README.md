Website hosting the NESP2 webmap

[![Build Status](https://travis-ci.com/rl-institut/NESP2_website.svg?branch=dev)](https://travis-ci.com/rl-institut/NESP2_website)

## Getting started

After cloning this repository, checkout the `dev` branch
```
git checkout dev
```

Create a virtual environment (with python3), then
```
pip3 install -r app/requirements.txt
```

Pull the latest changes from the [maps repository](https://github.com/rl-institut/NESP2)
```
python3 app/setup_maps.py
```

Start the app with  
```
python3 app/index.py
```

## Deploy on docker (instructions for ubuntu)
0. create a `app/instance/config.py` file with the line `SECRET_KEY = '<your secret key>'`.
If needed, you can generate a key with `python -c 'import os; print(os.urandom(16))'`)
1. install [docker](https://docs.docker.com/v17.09/engine/installation/linux/docker-ce/ubuntu/#install-docker-ce-1) and [docker-compose](https://docs.docker.com/compose/install/)

### With simple Dockerfile
1. `sudo docker build -t nesp2_website .`
2. `sudo docker run -rm -p 5000:5000 nesp2_website` you can use the `--build-arg` command to provide the postgresql login infos
3. Access the website at localhost:5000
4. to stop the service simply `ctrl + c` in the terminal from point 2.
### With docker-compose
1. `sudo docker-compose up -d --build`
2. your app is available at `0.0.0.0:5000` or `localhost:5000`
3. Access the website at localhost:5000
4. to stop the service `sudo docker-compose down`

In case something goes wrong, use `sudo docker logs nesp2_website` to check the logs
