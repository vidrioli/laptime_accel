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

 The [CarCreate](CarCreate.py) file is used to configure vehilce parameters, predefinec cars are available with paramaeters set to mimic real eForce Prague Formula vehicles. The [runLapTime](runLapTime.py) file contains the simulation code, the user can select numerical integration method (Euler or RK4) and simulate the acceleration event. The results are plotted and animated using matplotlib. The [PostProcessor](PostProcessor.py) file contains the plotting and animation code. 

 ## User Guide for single simulation

 1. If you want to create a new car, you can add it to the predefined cars dictionary in [CarCreate](CarCreate.py) along with it's parameters or pass the capameters to the create_car function 
 2. create an instance of Car, Solver(Car needs to be passed to Solver)
 3. the simualtion will be computed after calling the simulate_accel method of class Solver with parameters:
    - distance: distance of the acceleration event in meters
    - solver_type: numerical integrator type ('rk4' or 'euler' implemented)
    - dt: time step for the simulation (recommended maximum 0.001 s)
 4. the results can be plotted and animated using the PostProcessor class, which takes the results from the Solver class as input. The delay parameter in Animation method can be used to adjust the speed of the animation (default is 0.5 ms between frames)
 5. These are already implemented in the [runLapTime](runLapTime.py) file as an example.

 ## User Guide for sensitivity analysis

1. Same as single simulation, create an instance of Car
2. create an instance of Analyzer class, which takes the Car instance as input
3. call self.sesitivity method with parameters:
    - delta: percentage change of the parameter to be analyzed (e.g. 0.1 for 10% increase)
    - distance: distance of the acceleration event in meters
    - solver_type: numerical integrator type ('rk4' or 'euler' implemented)
    - dt: time step for the simulation (recommended maximum 0.001 s)