import numpy as np
import customtkinter as ctk
from functions import *
from color_simulate_functions import *
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Rectangle
from solver import dimensionless_system
from scipy.integrate import solve_ivp
import messagebox as mb

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.geometry("1000x600")

for i in range(1, 9):
    root.grid_columnconfigure(i, weight=1)

e1 = createEntry(root, "[BrO₃⁻]", 1, 1)
e2 = createEntry(root, "[HBrO2]", 1, 3)
e3 = createEntry(root, "[Br-]", 1, 5)
e4 = createEntry(root, "[Fe3+]", 1, 7)

figure = plt.Figure(figsize=(15, 8))
subplot = figure.add_subplot(211)
subplot2 = figure.add_subplot(212)

def plotGraph():
    try:
        solution = solve_ivp(dimensionless_system, (0, 50), [float(e2[1].get()), float(e3[1].get()), float(e4[1].get())], args=(2   , 3e6, 42  , 3e3, 1, float(e1[1].get()), 0.75), method='LSODA', t_eval=np.linspace(0, 50, 100000))
        assert float(e1[1].get()) >= 0 and float(e2[1].get()) >= 0 and float(e3[1].get()) >= 0 and float(e4[1].get()) >= 0  

        subplot.clear()
        subplot.plot(solution.t, np.log10(solution.y[0]), label='log10([HBrO2])', color='blue')
        subplot.plot(solution.t, np.log10(solution.y[1]), label='log10([Br-])', color='green')
        subplot.plot(solution.t, np.log10(solution.y[2]), label='log10([Fe3+])', color='red')
        subplot.set_xlabel('Time')
        subplot.set_ylabel('log10(Concentration)')
        subplot.legend()
        mat_color_over_time = color_over_time_fxn(solution)
        
        #Color ribbon as temporary representation of solution color
        plot_rgb_line_on_subplot(subplot2, solution.t, mat_color_over_time)

        canvas = FigureCanvasTkAgg(figure, root)
        canvas.draw()
        canvas.get_tk_widget().grid(row=5, column=1, padx=20, columnspan=8)
    except ValueError:
        mb.showerror(title = "Invalid Input", message = "Please enter a numeric value for all four compounds.")
    except AssertionError:
        mb.showerror(title = "Invalid Input", message = "Please enter a positive number.")

storeInitialValuesButton = ctk.CTkButton(root, text="Calculate", command=plotGraph)
storeInitialValuesButton.grid(row=2, column=8)

root.mainloop()
