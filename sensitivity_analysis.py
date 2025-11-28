from CarCreate import create_car
from matplotlib import pyplot as plt
import numpy as np
from runLapTime import Solver
from tqdm import tqdm

class Analyzer:
    def __init__(self,car): # initialize with base car
        self.car = car

    def sensitivity(self,delta,distance,solver_type='rk4', dt=0.001):
        params_dict = vars(self.car)
        base_results = Solver(self.car).simulate_accel(distance,solver_type,dt) # simulate base car
        results_dict = {'baseline': base_results} # store baseline results in dictionary because number of steps will vary
        print(f"Testing sensitivity for parameters: {params_dict.keys()}")
        # MAIN LOOP OVER PARAMETERS
        with tqdm(total=(len(params_dict)-1), leave=True,  colour='green') as pbar:  # add progress bar, needs to encapsulate the while loop
            for name, value in params_dict.items():  # iterate over parameters in the dictionary
                if type(value) in [int, float]:
                    setattr(self.car, name, value * (1+delta))  # increase parameter by delta
                    results_delta = Solver(self.car).simulate_accel(distance,solver_type,dt) # simulate with increased parameter
                    results_dict[f'{name}_plus'] = results_delta
                    setattr(self.car, name, value )  # reset parameter to base value   
                else:
                    continue
                pbar.update(1) # update progress bar
        return results_dict
            

avto = create_car('CTU24')
analysis = Analyzer(avto)
results_dict=analysis.sensitivity(0.1,75,'rk4',0.001) # 10% parameter change, 75m distance, rk4 solver

# prepare arrays of labes and times
labels = np.array([])
final_times = np.array([])  

for param, results in results_dict.items(): #iterate over results dictionary
    final_time = results[-1,2]      
    labels = np.append(labels,param)
    final_times = np.append(final_times,final_time)

final_times = final_times - final_times[0]  # calculate time difference from baseline


# Make the bar chart
plt.figure(figsize=(10,6))
plt.bar(labels, final_times, color='orange')
plt.ylabel("Final Simulation Time diff from baseline [s]")
plt.xlabel("Simulation Case")
plt.title("Effect of 10% Parameter Increase on Final Time")
plt.xticks(rotation=45)
plt.tight_layout()
plt.grid()
plt.show()