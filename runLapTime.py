
from CarCreate import create_car
from matplotlib import pyplot as plt
import numpy as np
from tqdm import tqdm
from matplotlib.animation import FuncAnimation


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

    def simulate_accel(self, distance,solver_type='euler', dt=0.001):
        v,x,t,a,E = 0,0,0,0,0 # initial speed, position, time, acceleration, energy
        Y = np.array([x,v])  # initial state vector
        data = []  # list to store simulation results

        integrator = get_integrator(solver_type)

        
        while x < distance:
                
                 x_new, v_new = integrator.integrate(self.state_derivative, Y, t, dt,a)
                 a, Fdrag, Frolling, Fgear, Ftractive, F_total = self.compute_forces(v_new, a)
                 #dE = v * Ftractive
                 #E_new = integrator.integrate(dE, E, dt) # cumulative energy used by vehicle
                 E_new=0
                 t_new = t + dt
                 data.append([v_new, x_new, t_new,Fdrag,Frolling,Fgear,Ftractive,F_total,E_new,a]) #store simulated data in list each new timestep is a new list
                 v, x, t = v_new, x_new, t_new
                 Y = np.array([x, v]) # update state vector
                 #time.sleep(0.01)
    
        results = np.array(data)  # convert list to numpy array
        return results

class PostProcessor:
    def __init__(self, results):
        self.results = results 
        self.velocity = self.results[:,0]    # save as attributes for reuse in other methods
        self.position = self.results[:,1]
        self.time = self.results[:,2]
        self.Fdrag = self.results[:,3]
        self.Frolling = self.results[:,4]
        self.Fgear = self.results[:,5]
        self.Ftractive = self.results[:,6]
        self.F_total = self.results[:,7]
        self.a = self.results[:,9]
        self.loss_force = self.Fdrag + self.Frolling + self.Fgear   
        self.P = self.Ftractive * self.velocity  
        self.P_loss = self.loss_force * self.velocity     
        print(f"Simulation complete. Final time is {round(self.time[-1],3)} s at {round(self.velocity[-1],2)} m/s")


    def Animation(self):
       

        fig = plt.figure(figsize=(12,8))
        gs = fig.add_gridspec(2, 2)
        fig.canvas.manager.set_window_title('Acceleration Sim Animation')

        self.ax_track = fig.add_subplot(gs[0, 0]) # plot simple track and car as red dot
        self.ax_track.set_xlim(0, self.position[-1])
        self.ax_track.set_ylim(-1, 1)
        self.track_line, = self.ax_track.plot([0, self.position[-1]], [0, 0], 'k--', lw=2) # comma to only return the first element (line object)
        self.car_dot, = self.ax_track.plot([], [], 'ro', markersize=14)
        self.ax_track.set_title("Car on Track")
        self.ax_track.axis('off')

        self.ax_vel = fig.add_subplot(gs[0, 1])
        self.ax_vel.set_xlim(np.min(self.time), np.max(self.time))
        self.ax_vel.set_ylim(np.min(self.velocity), np.max(self.velocity)+3)
        self.vel_line, = self.ax_vel.plot([], [], 'b-')
        self.ax_vel.set_xlabel("Time (s)")
        self.ax_vel.set_ylabel("Velocity (m/s)")
        self.ax_vel.set_title("Velocity vs Time")
        self.ax_vel.grid()

        self.ax_acc = fig.add_subplot(gs[1, 0])
        self.ax_acc.set_xlim(np.min(self.time), np.max(self.time))
        self.ax_acc.set_ylim(np.min(self.a)-1, np.max(self.a) + 1)
        self.acc_line, = self.ax_acc.plot([], [], 'g-', lw=1.5)
        self.ax_acc.set_xlabel("Time (s)")
        self.ax_acc.set_ylabel("Acceleration (m/s$^2$)")
        self.ax_acc.set_title("Acceleration vs Time")  
        self.ax_acc.grid()

        self.ax_bar = fig.add_subplot(gs[1, 1])
        self.bar_labels = ['Tractive', 'Loss', 'Net']
        self.bar_values = [0,0,0]
        self.bars = self.ax_bar.barh(self.bar_labels, self.bar_values, color=['tab:green', 'tab:red', 'tab:blue'])
        self.ax_bar.set_xlim(min(-np.max(self.Ftractive), -np.max(self.loss_force)),np.max(self.Ftractive)*1.1)
        self.ax_bar.set_title('Forces (Animated)')
        self.ax_bar.set_xlabel('Force (N)')

        # Animate
        self.anim = FuncAnimation(
            fig, self.update,
            frames=len(self.time),
            interval=0.5, blit=True, repeat=False)
        plt.tight_layout()
        #plt.show()

    def update(self, frame):
        
        self.car_dot.set_data([self.position[frame]], [0]) #modify car dot object data for efficient animation, without needing to redraw entire plot
        self.vel_line.set_data(self.time[:frame], self.velocity[:frame])
        self.acc_line.set_data(self.time[:frame], self.a[:frame])

        self.bars[0].set_width(self.Ftractive[frame])
        self.bars[1].set_width(self.loss_force[frame])
        self.bars[2].set_width(self.F_total[frame])

        return self.car_dot, self.vel_line, self.acc_line, *self.bars
    
    def Plot_Forces(self):
        F_max_idx = np.argmax(self.Ftractive)
        fig, (ax1, ax2) = plt.subplots(2, sharex=True, figsize=(10,8),)
        fig.canvas.manager.set_window_title('Forces Plot')
        ax1.plot(self.time, self.F_total, label='Net Force')
        ax1.plot(self.time, self.Fdrag, label='Drag Force')
        ax1.plot(self.time, self.Frolling, label='Rolling Resistance')
        ax1.plot(self.time, self.Fgear, label='Gearbox Resistance')
        ax1.vlines(self.time[F_max_idx],0,(np.max(self.Ftractive))*1.1, color='black', linestyle='--', label='Max Tractive Force Point')
        ax1.legend()
        ax1.set_title('Forces during Acceleration Simulation')
        ax1.set_ylabel('Force (N)')
        ax1.set_xlabel('Time (s)')
        ax1.grid()

        ax2.plot(self.time, self.P / 1000, 'g-', label='Tractive Power')
        ax2.plot(self.time, self.P_loss / 1000, 'r-', label='Power Losses')
        ax2.vlines(self.time[F_max_idx],0,(np.max(self.P / 1000))*1.1, color='black', linestyle='--', label='Tractive Power Limit Reached')
        ax2.set_ylabel('Power (kW)')
        ax2.set_xlabel('Time (s)')
        ax2.legend()
        ax2.set_title('Power during Acceleration Simulation')
        ax2.grid()
        #plt.show()  

    def show_all(self):
        plt.show() # show all plots and animations at the same time

    def Plot_performance(self):
        plt.figure(figsize=(10,6))
        plt.plot(self.position, self.velocity, 'b-')
        plt.title("Velocity vs Position")
        plt.xlabel("Position (m)")
        plt.ylabel("Velocity (m/s)")
        plt.grid()
        plt.show()


    

if __name__ == "__main__":  #run simulation only if runLapTime.py is ran directly, not when imported as module        
    avto = create_car('CTU25')
    sim = Solver(avto)
    result = sim.simulate_accel(75,'euler')  # simulate acceleration over 75 meters

    pp = PostProcessor(result)

    pp.Plot_performance
    pp.Plot_Forces()
    pp.Animation()
    pp.show_all()


