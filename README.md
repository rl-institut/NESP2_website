Website hosting the NESP2 webmap

## Getting started

After cloning this repository, checkout the `dev` branch
```
git checkout dev
```

Create a virtual environment (with python3), then
```
pip3 install -r app/requirements.txt
```

Start the app with  
```
python3 app/index.py
```

## Deploy on docker (instructions for ubuntu)
0. create a `app/instance/config.py` with the line `SECRET_KEY = '<your secret key>'`.
If needed, you can generate a key with `python -c 'import os; print(os.urandom(16))'`)
1. install [docker](https://docs.docker.com/v17.09/engine/installation/linux/docker-ce/ubuntu/#install-docker-ce-1) and [docker-compose](https://docs.docker.com/compose/install/)
2. `sudo docker-compose up -d --build`
3. your app is available at `0.0.0.0:5000` or `localhost:5000`
4. to stop the service `sudo docker-compose down`

In case something goes wrong, use `sudo docker logs nesp2_website` to check the logs