# SimApi Building Energy Co-Simulation Platform

This project aims to update and re-design an existing project found at [SimAPI repo](https://github.com/ElsevierSoftwareX/SOFTX_2018_29).
The objective of this project is to re-design and update the linked project using python, Django rest framework, 
Celery, Docker, and pyFMI to create an application capable of co-simulation between an Energy Management System and
a Functional Mock-Up Unit. The end goal is to deploy the project on a Docker swarm and simulate multiple fmu models
simultaneously. 

## Prerequisites
Version of docker and docker-compose 
```
Docker
- version >= 18.09.9

Docker-compose
- version >= 1.25.0
```


### Project structure

``` 
.
├── doc
│   ├── dev_requirements.txt
│   ├── docker_commands.txt
│   └── ER_Diagram.png
├── initialize_model.py     # Run Script to initialize models
├── LICENSE
├── README.md
├── run_initialized_model.py    # Run Script to simulate initialized models
├── src
│   ├── docker-compose.yml
│   ├── simapi_simulation   # root folder for FMU related files
│   │   ├── docker-compose.yml
│   │   ├── fmu_generator  
│   │   │   ├── celeryconfig.py
│   │   │   ├── docker-compose.yml
│   │   │   ├── Dockerfile
│   │   │   ├── Energy+.idd
│   │   │   ├── energy_plus_to_fmu.py
│   │   │   ├── fmu_volume_monitor.py
│   │   │   ├── generator_api.py
│   │   │   ├── generator_tasks.py
│   │   │   ├── requirements.txt
│   │   │   └── run.sh
│   │   └── fmu_simulator
│   │       ├── celeryconfig.py
│   │       ├── conda_requirements.txt
│   │       ├── docker-compose.yml
│   │       ├── Dockerfile
│   │       ├── fmu_location
│   │       ├── fmu_location_monitor.py
│   │       ├── __init__.py
│   │       ├── requirements.txt
│   │       ├── run.sh
│   │       ├── simulation_process.py
│   │       ├── simulator
│   │       │   ├── simulation_obj.py
│   │       │   └── test_simulation_obj.py
│   │       ├── simulator_api
│   │       │   ├── generator_client.py
│   │       │   └── sim_api.py
│   │       ├── simulator_tasks.py
│   │       ├── store_incoming_json
│   │       │   └── time_step.txt
│   │       ├── volume
│   │       └── volume_monitor.py
│   └── simapi_web      # Root folder for django REST API
│       ├── Dockerfile
│       ├── manage.py
│       ├── Media
│       ├── requirements.txt
│       ├── rest_api
│       │   ├── admin.py
│       │   ├── apps.py
│       │   ├── __init__.py
│       │   ├── migrations
│       │   │   ├── 0001_initial.py
│       │   │   ├── __init__.py
│       │   ├── models.py
│       │   ├── permissions.py
│       │   ├── schema.py
│       │   ├── serializers.py
│       │   ├── tasks.py
│       │   ├── tests
│       │   │   ├── __init__.py
│       │   │   ├── test_models.py
│       │   │   └── test_views.py
│       │   ├── urls.py
│       │   └── views.py
│       └── simapi_web
│           ├── asgi.py
│           ├── celery.py
│           ├── __init__.py
│           ├── schema.py
│           ├── settings.py
│           ├── urls.py
│           └── wsgi.py
└── test_setup_files
    ├── update.epw
    └── update.idf

```

### API Database ER Diagram
![ER Diagram](doc/ER_Diagram.png)

## Instructions
To build and run the containers navigate to src folder and type in a terminal

```
docker-compose build

Once build is finished bring up the db container to initialize it. Only needed for the first time after building.

docker-compose up db -d

Then bring the rest of the system up. No -d flag as you will need to see the output.

NOTE: To run multiple simulations run docker-compose up --scale simulator=n, where n is the desired number of simulations

For a single simulation run

docker-compose up

On Linux sudo will be needed
```

### simulator
Once the system is up and ready you should see similar output in the window running docker-compose

```
generator           | [2020-04-05 22:09:08,274: INFO/MainProcess] sync with celery@f06006b0333b
simulator_5         | [2020-04-05 22:09:08,274: INFO/MainProcess] sync with celery@f06006b0333b
web                 | [2020-04-05 22:09:08,274: INFO/MainProcess] sync with celery@f06006b0333b
simulator_1         | [2020-04-05 22:09:08,274: INFO/MainProcess] sync with celery@f06006b0333b
simulator_2         | [2020-04-05 22:09:08,275: INFO/MainProcess] sync with celery@f06006b0333b
simulator_4         | [2020-04-05 22:09:08,275: INFO/MainProcess] sync with celery@f06006b0333b
simulator_3         | [2020-04-05 22:09:09,310: INFO/MainProcess] mingle: sync with 6 nodes
simulator_3         | [2020-04-05 22:09:09,311: INFO/MainProcess] mingle: sync complete
simulator_3         | [2020-04-05 22:09:09,412: INFO/MainProcess] celery@f06006b0333b ready.

```
The system is now ready to initialize the models.

To Run the initialize_model.py script open terminal window in the project root folder and run (need to add dependencies example polling2)

```
python initialize_model.py model_name
```

Where model_name is a user defined string argument for the script.

Check the output in the docker-compose window once the simulation object is ready to receive inputs you will see the output below

```
simulator_1         | Starting Simulation at 01/01/2011 for RUNPERIOD 1
simulator_1         | ExternalInterface starts first data exchange
```

From the project root folder run

```
python run_initialized_model.py model_name
```

Where model_name is the same value passed to initialize_model.py.

Outputs are printed for each model on the same time step. Check the window running docker-compose for debugging information.

Once the simulations have ended you will see the output 
```
simulator_1         | Writing tabular output file results using HTML format.
simulator_1         | Writing final SQL reports
simulator_1         |  ReadVarsESO program starting.
simulator_1         |  ReadVars Run Time=00hr 00min  0.05sec
simulator_1         |  ReadVarsESO program completed successfully.
simulator_1         |  ReadVarsESO program starting.
simulator_1         |  ReadVars Run Time=00hr 00min  0.02sec
simulator_1         |  ReadVarsESO program completed successfully.
simulator_1         | EnergyPlus Run Time=00hr 08min  5.90sec
simulator_1         | EnergyPlus Completed Successfully.
simulator_1         | [INFO][Slave] [ok][FMU status:OK] freeInstanceResources: Slave will be freed.

```

Bring down the containers with ctrl-c

Use docker-compose up --scale simulator=n to test different values for n after 5 memory may be an issue depending
on host machine specs. Tested up to 25 simulations.

To wipe the data from the database and containers run 
```
docker-compose down --volumes
```
Then initialize the database again with
```
docker-compose up -d db 
```



## Project Development

If you would like to run the Django API or simulation scripts without docker the following steps are required.

1. Install python Anaconda

2. Create a virtual env python=3.7

3. Run conda commands

   conda config --append channels conda-forge
   
   conda install -c conda-forge assimulo
   
   conda install -c https://conda.binstar.org/chria pyfmi

4. pip install -r [dev_requirements.txt](doc/dev_requirements.txt) to install project dependencies

If running the Django project without Docker is all that is required then you can stop here. 

If you would also like to run simulation scripts then it is necessary to install energyPlus on your machine. 

Version 9 is required.

For windows installation see [energyPlus windows](https://energyplus.net/installation-windows)

For Linux installation see  [energyPlus Linux](https://energyplus.net/installation-linux)






