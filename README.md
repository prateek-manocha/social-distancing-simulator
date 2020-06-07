# Social-Sistancing-Simulator
An artificial social distancing simulator to validate the need of social distancing to slow the spread of covid-19.
Inspired by: https://www.washingtonpost.com/graphics/2020/world/corona-simulator/

__Currently working on adding other factors that govern the real life scenario, making a web based interface for the same.__

## Simulation 
In the simulation, given the below set of parameters, each person is assumed to move in a random direction with random velocity, except the people following social distancing(having black ring to distingush them) who are immobile. 

### Parameters:
The following parameters can be altered in params.py file.
* __Ground_size__: To change the area of the box movement is confined to.
* __Population__: To control the total number of healthy population at the start of simulation.
* __Init_sick__: Initial sick people at the start.
* __Recovery_time__: Constant recovery time, after which an infected person will become recovered.
* __Radii__: Safe social distancing distance each person needs to maintain.
* __Hospital_beds__: Total nu,ber of available hospital beds.
* __Social_dist__: Total number of people following social distancing.

### Understanding Simulation
The following color code has been used to categorise people:
* __Green__: Healthy people, not yet infected.
* __Red__: Sick people, currently suffering from covid-19.
* __Blue__: People who have recovred from the sickness and hence immune to it.
* __Black__: People who lost their life due to lack of medical assitance.
* __Black_Ring__: Particles having black edgerings are following social distaning, hence are immobile.

In the simulation, we assume a city with people(#population) moving randomly at any give moment. The city has a hospital with capacity equal to #Hospital_beds. 
To begin with, we assume #Init_sick people to be infected(color red), who pass on the disease when they come in contact with healthy people(color green). Any infected person is tried to get admitted in the hospital is there are any vacannies. IF the person gets medical assitance within the recovery time, they get recovered(color changes to blue). As people get recovered, there beds/position in hospital are available for incoming infected people.
However, if the person doesn't get medical assitance within the recovery time due to unavailability of bed in hospital, they die due to infection.

### Results
The simulation was runned for three experiments with the different percentage of the population following social distancing:
* 0%: No one follows social distancing, free movement for all.
* 25%: 25% of people follow social distancing
* 50%: 50% of people follow social distancing
* 75%: 75% of people follow social distancing
Videos available at: 

As clearly depectible in the images below, as social distancing increases, it takes much longer for everyone to get infected and hospitals can treat all patients because they don’t arrive all at once. Thus,#dead people decreases with increase in social distancing.


#### Tabular comparision:
Final results after everyone becomes imune to the sickness:

Social Distancing % | 0% | 25% | 50% |75%
------------ | -------------|------------ | -------------|------------ 
Sick | 0 | 0 | 0 | 0 
Healthy | 0 | 1 |0| 48
Recovered| 81 | 85 |0|53
Dead | 20 | 15 |0|0


