#!/bin/bash

cd /home/fmu/code/energy/test && \
python  /home/fmu/code/energy/Scripts/EnergyPlusToFMU.py -d -i /home/fmu/code/Energy+.idd -w /home/fmu/code/USA.epw \
/home/fmu/code/_fmu-export-variable.idf && \
./idf-to-fmu-export-prep-linux /home/fmu/code/Energy+.idd /home/fmu/code/_fmu-export-variable.idf