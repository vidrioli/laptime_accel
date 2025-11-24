# laptime_accel
## Description

Laptime simulation for Formula Student Acceleration event. The user will be able to adjust simulation parameters. The base paramater will be set to mimick a realistic FS vehicle during the event:
 - 75 m standing start drag race
 - 80 kW Maximum combined motor power, as per Formula Student germany rules
 - Vehicle parameters similar to eForce Prague Formula CTU.24 racecar (3rd Place Overall FSG24)

## Assumptions made

 - twin track vehicle model 
 - (no lateral load transfer since we are going in a straight line)
 - uses longitudinal load transfer
 - no wheel dynamics, optimal slip ratio is assumed at all time
 - tire $\mu_x$ is a linear function of normal load
 - no field weakening, ideal PMSM motor curve
 - no suspension pitch dynamics
 - linear rolling resistance and gearbox drag 

 ## Simulation

 The [CarCreate](CarCreate.py) file is used to configure vehilce parameters, predefinec cars are available with paramaeters set to mimic real eForce Prague Formula vehicles. The [runLapTime](runLapTime.py) file contains the simulation code, the user can select numerical integration method (Euler or RK4) and simulate the acceleration event. The results are plotted using matplotlib.

 ## User Guide

 1. If you want to create a new car, you can add it to the predefined cars dictionary in [CarCreate](CarCreate.py) along with it's parameters or pass the capameters to the create_car function 
 2. create an instance of Car, Solver(Car needs to be passed to Solver)
 3. the simualtion will be computed after calling the simulate_accel method of class Solver with the integrator type (RK4 or Euler for now) and the distance of the acceleration event.