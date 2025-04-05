# Simulated based on the 3-variable dimensionless system of paper by Jie et al
# Comput Visual Sci (2009) 12:227–234  10.1007/s00791-008-0092-2
# Solver: LSODA

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Define the system of differential equations
# A: BrO3-, X: HBrO2, Y: Br-, Z: Fe3+, 
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
