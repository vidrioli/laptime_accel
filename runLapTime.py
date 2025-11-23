
from CarCreate import create_car
from matplotlib import pyplot as plt
import numpy as np
from tqdm import tqdm


class Euler:   # simple Euler integrator class
    def integrate(self, f, y0, t, dt,a):
        y_new = y0 + f(y0,a)*dt
        return y_new
    
class RK4:  # runge kutta integrator class
    def integrate(self, f, y0, t, dt,a):
        k1 = f(y0,a)
        k2 = f(y0 + 0.5 * dt * k1,a)
        k3 = f(y0 + 0.5 * dt * k2,a)
        k4 = f(y0 + dt * k3,a)    
        y_new = y0 + (dt / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
        return y_new


def get_integrator(name=str):  # class factory function, returns instance of integrator class
        if name == 'euler':
            return Euler()
        elif name == 'rk4':
            return RK4()
        else:
            raise ValueError(f"Unknown integrator type: {name}")



class Solver:
    def __init__(self, car):
        self.car = car

    def compute_forces(self,v,a): #force calculation function
        Fdrag = self.car.Fd(v)
        Frolling = self.car.Frr()
        Fgear = self.car.Fgear(v)
        Ftractive = self.car.Ftractive(v,a)
        F_total = Ftractive - Fdrag - Frolling - Fgear # net force acting on the car
        a_new = F_total / self.car.m  # acceleration
        return a_new, Fdrag, Frolling, Fgear, Ftractive, F_total

    def state_derivative(self,Y,a):
        x_new, v_new = Y # unpack state vector
        a_new = self.compute_forces(v_new,a)[0]
        return np.array([v_new, a_new])  # return derivative of state vector

    def simulate_accel(self, distance,solver_type='euler', dt=0.0001):
        v,x,t,a,E = 0,0,0,0,0 # initial speed, position, time, acceleration, energy
        Y = np.array([x,v])  # initial state vector
        data = []  # list to store simulation results

        integrator = get_integrator(solver_type)

        with tqdm(total=distance, leave=True,  colour='green') as pbar:  # add progress bar, needs to encapsulate the while loop
            while x < distance:
                 
                
                 x_new, v_new = integrator.integrate(self.state_derivative, Y, t, dt,a)
                 a, Fdrag, Frolling, Fgear, Ftractive, F_total = self.compute_forces(v_new, a)
                 #dE = v * Ftractive
                 #E_new = integrator.integrate(dE, E, dt) # cumulative energy used by vehicle
                 E_new=0
                 t_new = t + dt
                 data.append([v_new, x_new, t_new,Fdrag,Frolling,Fgear,Ftractive,F_total,E_new]) #store simulated data in list each new timestep is a new list
                 v, x, t = v_new, x_new, t_new
                 Y = np.array([x, v]) # update state vector
                 #time.sleep(0.01)

                 pbar.update(v * dt) # update progress bar
    
        results = np.array(data)  # convert list to numpy array
        print(f"Simulation complete. Final time is {t} s at {v} m/s")
        return results
        
    
avto = create_car('CTU25')
sim = Solver(avto)
result = sim.simulate_accel(75,'rk4')  # simulate acceleration over 75 meters

# Extract data for plotting
time = result[:,2]
velocity = result[:,0]
position = result[:,1]
Fdrag = result[:,3]
Frolling = result[:,4]
Fgear = result[:,5]
Ftractive = result[:,6]
F_total = result[:,7]


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
plt.plot(time, F_total, label='Net Force')
plt.legend()
plt.show()