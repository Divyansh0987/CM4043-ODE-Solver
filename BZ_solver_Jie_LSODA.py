# Simulated based on the 3-variable dimensionless system of paper by Jie et al
# Comput Visual Sci (2009) 12:227–234  10.1007/s00791-008-0092-2
# Solver: LSODA

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import math

# Define the system of differential equations
# A: BrO3-, X: HBrO2, Y: Br-, Z: Ce4+, yellow
def dimensionless_system(t, z_val, k1, k2, k3, k4, k5, A, h):
    x, y, z = z_val

    # Additional parameter based on the paper
    eps = k1/k3
    p = (k1 * A) / k5
    q = (2 * k1 * k4) / (k2 * k3)
    
    # Define the differential equations
    dxdt = (x + y - x * y - q * x**2)/eps
    dydt = 2 * h * z - y - x * y
    dzdt = (x - z)/p
    
    return [dxdt, dydt, dzdt]

a = 0.001  # Initial condition for x
b = 0.001  # Initial condition for y
c = 0.04   # Initial condition for z
initial_conditions = [a, b, c]

parameter_sets = [
    (2   , 3e6, 66  , 3e3, 2 , 0.2, 0.75),  # parameter_set_1a
    (1.28, 3e6, 33.6, 3e3, 1    , 0.2, 0.75),  # parameter_set_1b
    (2   , 3e6, 42  , 3e3, 1    , 0.2, 0.75),  # parameter_set_1c
    (2   , 2e9, 1e4 , 4e7, 0.6, 0.2, 0.75)  # parameter_set_1d, unstable solution
]

#Weird behavior with k5 != 1, but idk enough to fix
# (k1, k2, k3, k4, k5, A, h)
# h: check definition in paper, important parameters

t_span = (0, 50)
t_eval = np.linspace(0, 50, 100000)

fig, axs = plt.subplots(4, 1, figsize=(10, 16))

# Loop through parameter sets and plot each one on a different subplot
for i, param_set in enumerate(parameter_sets):
    # Solve the system with the current parameter set

    solution = solve_ivp(dimensionless_system, t_span, initial_conditions, args=param_set,
                         method='LSODA', t_eval=t_eval)
    
    # Plot the log10 values of X, Y, Z for the current parameter set
    axs[i].plot(solution.t, np.log10(solution.y[0]), label='log10(X)', color='blue')
    axs[i].plot(solution.t, np.log10(solution.y[1]), label='log10(Y)', color='green')
    axs[i].plot(solution.t, np.log10(solution.y[2]), label='log10(Z)', color='red')
    
    # Set titles and labels for each subplot
    axs[i].set_title(f'Log10 of BZ Reaction Dynamics - Parameter Set {chr(97+i)}')
    axs[i].set_xlabel('Time')
    axs[i].set_ylabel('log10(Concentration)')
    axs[i].legend()

# Adjust layout to avoid overlap
plt.tight_layout()
plt.show()