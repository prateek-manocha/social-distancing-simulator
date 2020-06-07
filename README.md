# Social-Distancing-Simulator
An artificial social distancing simulator to validate the need for social distancing to slow the spread of COVID-19.

Inspired by: https://www.washingtonpost.com/graphics/2020/world/corona-simulator/

__Currently working on adding other factors that govern the real-life scenario, making a web-based interface for the same.__

## Simulation 
In the simulation, given the below set of parameters, each person is assumed to move in a random direction with random velocity, except the people following social distancing(having a black ring to distinguish them) who are immobile. 

### Parameters:
The following parameters can be altered in params.py file.
* __Ground_size__: To change the area of the box movement is confined to.
* __Population__: To control the total number of people at the start of the simulation.
* __Init_sick__: Initial sick people at the start.
* __Recovery_time__: Constant recovery time, after which an infected person will become recovered.
* __Radii__: Safe social distancing distance each person needs to maintain.
* __Hospital_beds__: Total number of available hospital beds.
* __Social_dist__: Total number of people following social distancing.

### Understanding Simulation
The following color code has been used to categorize people:
* __Green__: Healthy people, not yet infected.
* __Red__: Sick people, currently suffering from COVID-19.
* __Blue__: People who have recovered from the sickness and hence immune to it.
* __Black__: People who lost their life due to lack of medical assistance.
* __Black_Ring__: Particles having black edge rings are following social distancing, hence are immobile.

In the simulation, we assume a city with people(#population) moving randomly at any given moment. The city also has a hospital with a capacity equal to #Hospital_beds. 
To begin with, we assume #Init_sick people to be infected(color red), who pass on the disease when they come in contact with healthy people(color green). Any infected person is tried to get admitted to the hospital is there are any vacancies. If the person receives medical assistance within the recovery time, they get recovered(color changes to blue). As people get healed, their beds in the hospital are available for incoming infected people.
However, if the sick person doesn't get medical assistance within the recovery time due to the unavailability of bed in the hospital, they die due to infection.

### Results
The simulation was run for three experiments with a different percentage of the population following social distancing:
* 0%: No one follows social distancing, free movement for all.
* 25%: 25% of people follow social distancing
* 50%: 50% of people follow social distancing
* 75%: 75% of people follow social distancing

Values of parameters used:
* Ground_size: 4x2 box
* Population: 101
* Init_sick: 1
* Recovery_time: 1000frames
* Radii: 0.02
* Hospital_beds: 25

Videos available at: https://drive.google.com/drive/folders/1IWgoS3V3vq196AcWmMLBFvOrDbTduAri?usp=sharing

The images below clearly depict that as social distancing increases:
* It takes much longer for everyone to get infected.
* The peak for people getting infected decreases.
* As infected people don't increase suddenly(curve gets flat), hospitals can treat all patients because they don’t arrive all at once. Thus, #dead people decreases with an increase in social distancing.
* Due to some % of the population's immobile nature, we even have some healthy people at the end.

These simulations clearly show the need for social distancing in today's scenario and how it can help flatten the curve and help save lives.
The black line in stacked area graph shows the hospital capacity.
![0% social distancing](/images/final_0.png)
![25% social distancing](/images/final_25.png)
![50% social distancing](/images/final_50.png)
![75% social distancing](/images/final_75.png)

#### Tabular comparision:
Final results after everyone becomes immune to the sickness:

Social Distancing % | 0% | 25% | 50% |75%
------------ | -------------|------------ | -------------|------------ 
Sick | 0 | 0 | 0 | 0 
Healthy | 0 | 1 |12| 48
Recovered| 81 | 85 |77|53
Dead | 20 | 15 |12|0


