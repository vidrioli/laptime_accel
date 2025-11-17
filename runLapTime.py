
from CarCreate import create_car
from matplotlib import pyplot as plt
import numpy as np


avto = create_car('CTU24')


class Solver:
    def __init__(self, car):
        self.car = car

    def simulate_accel(self, distance, dt=0.01):
        v,x,t = 0,0,0 # initial speed, position, time
        data = []  # to store simulation results


        while x < distance:
            Fdrag = self.car.Fd(v)
            Frolling = self.car.Frr()
            Fgear = self.car.Fgear(v)
            Ftractive = self.car.Ftractive(v)
            F_total = Ftractive - Fdrag - Frolling - Fgear # net force acting on the car
            a = F_total / self.car.m  # acceleration
            v_new = v + a * dt
            x_new = x + v * dt
            t_new = t + dt

            data.append([v_new, x_new, t_new,Fdrag,Frolling,Fgear,Ftractive]) #store simulated data in list each new timestep is a new list
            v, x, t = v_new, x_new, t_new
    
        results = np.array(data)  # convert list to numpy array
        print(f"Simulation complete. Final time is {t} s at {v} m/s")
        return results
        
    

sim = Solver(avto)
result = sim.simulate_accel(75)  # simulate acceleration over 75 meters

# Extract data for plotting
time = result[:,2]
velocity = result[:,0]
position = result[:,1]
Fdrag = result[:,3]
Frolling = result[:,4]
Fgear = result[:,5]
Ftractive = result[:,6]

# Plot results
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.plot(time, velocity)
plt.title('Acceleration Simulation Results')
plt.ylabel('Velocity (m/s)')
plt.subplot(2, 1, 2)
plt.plot(time, position)
plt.xlabel('Time (s)')
plt.ylabel('Position (m)')
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 6))
plt.plot(time, Ftractive, label='Tractive Force')
plt.show()