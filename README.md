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
 - tire $mu_x$ is a linear function of normal load