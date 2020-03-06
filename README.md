# SimApi Building Energy Co-Simulation Platform

This project aims to develop a RestFul API for building energy management systems (EMS).

## Prerequisites
Having the correct versions of docker and docker-compose is essential
```
Docker
- version 18.09.9

Docker-compose
- version 1.25.0
```


### Project structure

```
.
└── src
    ├── docker-compose.yml
    ├── Dockerfile
    ├── simapi_simulation **# root directory for fmu related containers**
    │   ├── docker-compose.yml
    │   ├── fmu_generator **# container generates a .fmu. Place .idf, .epw, .idd in this folder**
    │   │   ├── docker-compose.yml
    │   │   ├── Dockerfile
    │   │   ├── Energy+.idd
    │   │   ├── _fmu-export-variable.idf 
    │   │   ├── run.sh
    │   │   ├── USA.epw
    │   │   └── volume **# .fmu and other energyPlusToFMU files generated here!**
    │   └── fmu_simulator **# Container simulates .fmu using pyFMI framework**
    │       ├── conda_requirements.txt
    │       ├── docker-compose.yml
    │       ├── Dockerfile
    │       ├── __init__.py
    │       ├── requirements.txt
    │       ├── simulator **# Root folder for simulation scripts**
    │       │   ├── _fmu_export_variable.fmu
    │       │   ├── __init__.py
    │       │   ├── json_generator.py
    │       │   ├── simulation_obj.py **# simulation object, initialize fmu model and do time_step**
    │       │   └── test_simulation_obj.py 
    │       ├── simulator_api **# Root folder for api client. Interface with API**
    │       │   └── __init__.py
    |       |   └── api_client.py 
    │       └── volume
    └── simapi_web **# Django project root**
        ├── manage.py
        ├── __pycache__
        │   └── manage.cpython-37.pyc
        ├── requirements.txt
        ├── rest_api **# Core of the Django project is the restAPI app**
        │   ├── admin.py
        │   ├── apps.py
        │   ├── __init__.py
        │   ├── middleware.py
        │   ├── migrations
        │   │   ├── 0001_initial.py
        │   │   ├── __init__.py
        │   ├── models.py **# See ER diagram for model overview**
        │   ├── permissions.py
        │   ├── serializers.py
        │   ├── tests **# Test coverage is high and all tests pass**
        │   │   ├── __init__.py
        │   │   ├── test_models.py
        │   │   └── test_views.py
        │   ├── urls.py
        │   └── views.py
        ├── simapi_web
        │   ├── asgi.py
        │   ├── __init__.py
        │   ├── settings.py
        │   ├── urls.py
        │   └── wsgi.py
        └── TODO.py


```

### API Database ER Diagram
![ER Diagram](doc/ER_Diagram.png)

## Instructions

To build and run the containers navigate to src folder and type in a terminal

```
docker-compose build

docker-compose up -d

On Linux sudo will be needed
```

The -d flag runs the containers in detached mode freeing the terminal allowing for access to each containers shell

## Working With Containers

The three main containers are web, simulator, and generator. The fourth is a postgres database container which the web container is a dependant.

```
Type "docker container ps" to ensure containers are running
```
#### web
The web container holds the Django restAPI. It is necessary to make database migrations and migrate.

docker command to **makemigrations** and **migrate** using Django **manage.py**
```
docker exec -it web python manage.py makemigrations

docker exec -it web python manage.py migrate
```

Next create a superuser
```
docker exec -it web python manage.py createsuperuser
```
Open http://127.0.0.1:8000/admin in a browser and log in as superuser to ensure everything is working.
Once the web container is working we can move onto the simulator container to interact with the API.

#### simulator
run command to enter simulation container shell

```
docker exec -it simulator /bin/bash
```
Test communication with web is possible
```
curl -v http://web:8000/user/
```
If the request is successful you will see json output of your superuser in the terminal.
There is two _sub-folders_ in the _current directory_, **simulator and simulator_api**.

Type
```
cd simulator
```
The **simulator** folder is where we place the .fmu model. fmu models are simulated using a 
simulation_obj see **simulation_obj.py**, also see **test_simulation_obj.py**

Run **test_simulation_obj.py** to see the output of some calls to simulation_obj.do_step
```
python test_simulation_obj.py
```
go back one directory using
```
cd ..
```
Go to folder simulation_api
```
cd simulation_api
```

This folder is the root of an API client script **api_client.py** this script tests the capability of this container 
to communicate with the web container. Running the script should POST data to the API endpoints. Will be required to 
edit the user data with your own superuser details.

The output will be printed to the shell. Expected output will be in json format
```
python api_client.py
```


#### generator

