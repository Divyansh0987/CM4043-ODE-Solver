import numpy as np
import customtkinter as ctk
from functions import *
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from solver import dimensionless_system
from scipy.integrate import solve_ivp

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.geometry("1000x600")

for i in range(1, 9):
    root.grid_columnconfigure(i, weight=1)

e1 = createEntry(root, "[BrO₃⁻]", 1, 1)
e2 = createEntry(root, "[HBrO2]", 1, 3)
e3 = createEntry(root, "[Br-]", 1, 7)
e4 = createEntry(root, "[Ce4+]", 1, 5)

figure = plt.Figure()
subplot = figure.add_subplot(111)

def plotGraph():
    solution = solve_ivp(dimensionless_system, (0, 50), [e2[1].get(), e3[1].get(), e4[1].get()], args=(2, 3e6, 66, 3e3, 2, 0.2, 0.75), method='LSODA', t_eval=np.linspace(0, 50, 100000))

    subplot.clear()
    subplot.plot(solution.t, np.log10(solution.y[0]), label='log10(X)', color='blue')
    subplot.plot(solution.t, np.log10(solution.y[1]), label='log10(Y)', color='green')
    subplot.plot(solution.t, np.log10(solution.y[2]), label='log10(Z)', color='red')
    subplot.set_xlabel('Time')
    subplot.set_ylabel('log10(Concentration)')
    subplot.legend()
    
    canvas = FigureCanvasTkAgg(figure, root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=5, column=1, padx=20, columnspan=8)

storeInitialValuesButton = ctk.CTkButton(root, text="Calculate", command=plotGraph)
storeInitialValuesButton.grid(row=2, column=8)

root.mainloop()
