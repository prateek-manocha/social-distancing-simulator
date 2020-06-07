# Social-Sistancing-Simulator
An artificial social distancing simulator toa show the need for following social distancing to slow the spread of covid-19.
Inspired by: https://www.washingtonpost.com/graphics/2020/world/corona-simulator/

**Currently working on adding other factors that govern the real life scenario.

## Simulation 
In the simulation, given the below set of parameters, each person is assumed to move in a random direction with random velocity, except the people following social distancing(having black ring to distingush them) who are immobile. 
### Parameters:
The following parameters can be tweaked in params.py file.
* __Ground_size__: To change the area of the box movement is confined to.
* __Population__: To control the total number of healthy population at the start of simulation.
* __Init_sick__: Initial sick people at the start.
* __Recovery_time__: Constant recovery time, after which an infected person will become recovered.
* __Radii__: Safe social distancing distance each person needs to maintain.
* __Hospital_beds__: Total nu,ber of available hospital beds.
* __Social_dist__: Total number of people following social distancing.

